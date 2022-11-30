import math
import textwrap
import time
import typing as tp
from string import Template

import config
import pandas as pd
import requests
import session
from pandas import json_normalize
from vkapi.exceptions import APIError


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
    # r_count = math.ceil(count / max_count)
    # if count:
    count = min(count, max_count)
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
        w_posts = w_posts + API.wall.get({{"owner_id":'{owner_id}',"domain": "{domain}","offset": offset,"count": c,"filter":"{filter}","extended":{extended},"fields":'{",".join(fields)}',"v":{config.VK_CONFIG["version"]}}})['items'];
        i=i+1;
    }};
    return {{'count': w_posts.length, 'items': w_posts}};"""
    # "domain":{domain},
    http_session = session.Session(base_url=config.VK_CONFIG["domain"])
    # data = {"code": code, "access_token": config.VK_CONFIG["access_token"], "v": config.VK_CONFIG["version"]}
    resp = http_session.post(
        "execute",
        data={
            "code": code,
            "access_token": config.VK_CONFIG["access_token"],
            "v": config.VK_CONFIG["version"],
        },
    )
    # payload = {'key1': 'value1', 'key2': 'value2'}
    # resp = requests.post(f'{config.VK_CONFIG["domain"]}/post/execute', data=payload)
    # payload_dict = {'key1': ['value1', 'value2']}
    # resp = requests.post('https://httpbin.org/post', data=payload_dict)
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
    posts = get_posts_2500(
        owner_id=owner_id,
        domain=domain,
        offset=offset,
        count=count,
        max_count=max_count,
        filter=filter,
        extended=extended,
        fields=fields,
    )
    time.sleep(1)
    return json_normalize(posts["items"])


if __name__ == "__main__":
    wall = get_wall_execute(domain="cs102py", count=1)
    # g = get_posts_2500(owner_id="290650846", count=5)
    b = 0
