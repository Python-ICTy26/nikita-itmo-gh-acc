import dataclasses
import json
import math
import time
import typing as tp

import config
import requests
import session
from exceptions import APIError
from tqdm import tqdm

# from vkapi import config, session
# from vkapi.exceptions import APIError


QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int,
    count: int = 5000,
    offset: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    arg_dict = {"user_id": user_id, "count": count, "offset": offset, "fields": fields}
    http_session = session.Session(base_url=config.VK_CONFIG["domain"])
    resp = http_session.get(
        "friends.get",
        access_token=config.VK_CONFIG["access_token"],
        **arg_dict,
        v=config.VK_CONFIG["version"],
        timeout=5
    )
    try:
        return FriendsResponse(**resp.json()["response"])
    except BaseException as error:
        raise APIError(message=str(error))


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    # active_users = [user["id"] for user in f_response.items if not user.get("deactivated")]
    try:
        req_count = math.ceil(len(target_uids) / 100)  # type: ignore
        target_uids = ",".join(list(map(str, target_uids)))  # type: ignore
    except TypeError:
        req_count = 1
    # if target_uid:
    #     if not target_uids:
    #         target_uids = []
    #     target_uids.append(target_uid)
    arg_dict = {
        "source_uid": source_uid,
        "target_uid": target_uid,
        "target_uids": target_uids,
        "order": order,
        "count": count,
        "offset": offset,
        "progress": progress,
    }
    http_session = session.Session(base_url=config.VK_CONFIG["domain"])
    result = []
    for req in range(req_count):
        resp = http_session.get(
            "friends.getMutual",
            access_token=config.VK_CONFIG["access_token"],
            **arg_dict,
            v=config.VK_CONFIG["version"]
        )
        new = resp.json()["response"]
        if target_uids:
            result.extend([MutualFriends(**f) for f in new])  # type: ignore
        else:
            kwargs = {
                "id": target_uid,
                "common_friends": new,
                "common_count": len(new),
            }  # type : ignore
            result.extend([MutualFriends(**kwargs)])  # type: ignore
        arg_dict["offset"] += 100
        if req % 2 == 0:
            time.sleep(1)
    return result
