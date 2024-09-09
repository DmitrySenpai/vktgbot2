from typing import Union

import re
import requests
from loguru import logger


def get_data_from_vk(
    vk_token: str, req_version: float, req_filter: str, req_count: int, VK_TO_TG: list
) -> Union[dict, None]:
    logger.info("Trying to get posts from VK.")
    list_post = {}
    for x in VK_TO_TG:
        match = re.search("^(club|public)(\d+)$", x[0])
        if match:
            source_param = {"owner_id": "-" + match.groups()[1]}
        else:
            source_param = {"domain": x[0]}
        response = requests.get(
            "https://api.vk.com/method/wall.get",
            params=dict(
                {
                    "access_token": vk_token,
                    "v": req_version,
                    "filter": req_filter,
                    "count": req_count,
                },
                **source_param,
            ),
        )
        data = response.json()
        if "response" in data:
            list_post[x[0]] = data["response"]["items"]
        elif "error" in data:
            logger.error("Error was detected when requesting data from VK: " f"{data['error']['error_msg']}")
        #return None
    if len(list_post) == 0:
        return None
    else:
        return list_post


def get_video_url(vk_token: str, req_version: float, owner_id: str, video_id: str, access_key: str) -> str:
    response = requests.get(
        "https://api.vk.com/method/video.get",
        params={
            "access_token": vk_token,
            "v": req_version,
            "videos": f"{owner_id}_{video_id}{'' if not access_key else f'_{access_key}'}",
        },
    )
    data = response.json()
    if "response" in data:
        return data["response"]["items"][0]["files"].get("external", "")
    elif "error" in data:
        logger.error(f"Error was detected when requesting data from VK: {data['error']['error_msg']}")
    return ""


def get_group_name(vk_token: str, req_version: float, owner_id) -> str:
    response = requests.get(
        "https://api.vk.com/method/groups.getById",
        params={
            "access_token": vk_token,
            "v": req_version,
            "group_id": owner_id,
        },
    )
    data = response.json()
    if "response" in data:
        #return data["response"][0]["name"]
        return data["response"]["groups"][0]["name"]
    elif "error" in data:
        logger.error(f"Error was detected when requesting data from VK: {data['error']['error_msg']}")
    return ""
