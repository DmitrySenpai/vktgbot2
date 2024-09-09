from typing import Union

from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from loguru import logger

import config, os
from api_requests import get_data_from_vk, get_group_name
from last_id import read_id, write_id
from parse_posts import parse_post
from send_posts import send_post
from tools import blacklist_check, prepare_temp_folder, whitelist_check


def start_script():
    if not os.path.isdir("last_id"):
        os.mkdir("last_id")

    bot = Bot(token=config.TG_BOT_TOKEN)
    dp = Dispatcher(bot)

    last_known_id = {}

    id_tg_channel = {}

    for x1 in config.VK_TO_TG:
        last_known_id[x1[0]] = read_id(x1[0])
        logger.info(f"Last known ID ({x1[0]}): {last_known_id[x1[0]]}")

    items: Union[dict, None] = get_data_from_vk(
        config.VK_TOKEN,
        config.REQ_VERSION,
        config.REQ_FILTER,
        config.REQ_COUNT,
        config.VK_TO_TG
    )
    if not items:
        return
    
    for x1 in config.VK_TO_TG:
        id_tg_channel[x1[0]] = x1[1]

    for x in items:
        if "is_pinned" in items[x][0]:
            items[x] = items[x][1:]
        logger.info(f"Got a few posts with IDs ({x}): {items[x][-1]['id']} - {items[x][0]['id']}.")

        new_last_id: int = items[x][0]["id"]

        if new_last_id > last_known_id[x]:
            for item in items[x][::-1]:
                item: dict
                if item["id"] <= last_known_id[x]:
                    continue
                logger.info(f"Working with post with ID: {item['id']}.")
                if blacklist_check(config.BLACKLIST, item["text"]):
                    continue
                if whitelist_check(config.WHITELIST, item["text"]):
                    continue
                if config.SKIP_ADS_POSTS and item["marked_as_ads"]:
                    logger.info("Post was skipped as an advertisement.")
                    continue
                if config.SKIP_COPYRIGHTED_POST and "copyright" in item:
                    logger.info("Post was skipped as an copyrighted post.")
                    continue

                item_parts = {"post": item}
                group_name = ""
                if "copy_history" in item and not config.SKIP_REPOSTS:
                    item_parts["repost"] = item["copy_history"][0]
                    group_name = get_group_name(
                        config.VK_TOKEN,
                        config.REQ_VERSION,
                        abs(item_parts["repost"]["owner_id"]),
                    )
                    logger.info("Detected repost in the post.")
                for item_part in item_parts:
                    prepare_temp_folder()
                    repost_exists: bool = True if len(item_parts) > 1 else False

                    logger.info(f"Starting parsing of the {item_part}")
                    parsed_post = parse_post(item_parts[item_part], repost_exists, item_part, group_name)
                    logger.info(f"Starting sending of the {item_part}")
                    executor.start(
                        dp,
                        send_post(
                            bot,
                            id_tg_channel[x],
                            parsed_post["text"],
                            parsed_post["photos"],
                            parsed_post["docs"],
                        ),
                    )

            write_id(new_last_id, x)
