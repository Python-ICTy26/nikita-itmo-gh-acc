import math
import textwrap
import time
import typing as tp
from string import Template
from unittest.mock import patch
from urllib.parse import unquote

import pandas as pd
import requests
import responses
import vkapi.config
from pandas import json_normalize
from vkapi.exceptions import APIError
from vkapi.session import Session


def get_posts_2500(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> tp.Dict[str, tp.Any]:
    if not fields:
        fields = []
    if count == 0:
        count = max_count
    r_count = math.ceil(count / 100)
    code = f"""var w_posts = [];
    var i = 0; 
    var c = {count};
    var offset;
    while (i < {r_count}) {{
        if (c > 100) {{c = c - 100;}}
        offset = {offset} + i * 100;
        w_posts = w_posts + API.wall.get({{"owner_id":'{owner_id}',"domain": "{domain}","offset": offset,"count": c,"filter":"{filter}","extended":{extended},"fields":'{",".join(fields)}',"v":{vkapi.config.VK_CONFIG["version"]}}})['items'];
        i=i+1;
    }};
    return {{'count': w_posts.length, 'items': w_posts}};"""
    # "domain":{domain},
    http_session = Session(base_url=vkapi.config.VK_CONFIG["domain"])
    # data = {"code": code, "access_token": config.VK_CONFIG["access_token"], "v": config.VK_CONFIG["version"]}
    resp = http_session.post(
        "execute",
        data={
            "code": code,
            "access_token": vkapi.config.VK_CONFIG["access_token"],
            "v": vkapi.config.VK_CONFIG["version"],
        },
    )
    return resp.json()["response"]


def get_wall_execute(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
    progress=None,
) -> pd.DataFrame:
    http_session = Session(base_url=vkapi.config.VK_CONFIG["domain"])
    if not fields:
        fields = []
    kw = {
        "owner_id": owner_id,
        "domain": domain,
        "offset": offset,
        "count": 1,
        "max_count": max_count,
        "filter": filter,
        "extended": extended,
        "fields": fields,
    }
    check_count = http_session.post(
        "execute",
        data={
            "code": f"""return API.wall.get({{
                            "owner_id": {owner_id},
                            "domain": "{domain},
                            "offset": {offset},
                            "count": 1,
                            "filter": {filter},
                            "extended": {extended},
                            "fields": {",".join(fields)},
                            "v": {vkapi.config.VK_CONFIG["version"]}}});
            """
        },
    )
    posts_count = 0
    if check_count.status_code == 200:
        posts_count = check_count.json()["response"]["count"]
    repeat = math.floor(posts_count / 2500) + 1
    for _ in range(repeat):
        kw["count"] = min(posts_count, 2500, count)
        posts = get_posts_2500(**kw)  # type: ignore
        posts_count -= 2500
        count -= 2500
        if count < 0:
            break
        time.sleep(1)
    if "items" in posts.keys():
        return json_normalize(posts["items"])
    else:
        return json_normalize(posts)


@responses.activate
def main():
    responses.add(
        responses.POST,
        "https://api.vk.com/method/execute",
        json={
            "response": {
                "count": 6000,
                "items": [],
            }
        },
        status=200,
    )
    start = time.time()
    with patch("vkapi.wall.get_posts_2500") as get_posts_2500:
        get_posts_2500.return_value = {}
        w = get_wall_execute(domain="cs102py", count=6000)
    end = time.time()
    # wall = get_wall_execute(domain="cs102py", count=1)
    # resp_body = unquote(responses.calls[0].request.body)
    a = 0


if __name__ == "__main__":
    main()
