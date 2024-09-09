from loguru import logger


def read_id(vk_id: str) -> int:
    try:
        return int(open("./last_id/" + vk_id + ".txt", "r").read())
    #except ValueError:
    except:
        #logger.info(
        #    "The value of the last identifier is incorrect. Please check the contents of the file 'last_id.txt'."
        #)
        #exit()
        return 0


def write_id(new_id: int, vk_id: str) -> None:
    open("./last_id/" + vk_id + ".txt", "w").write(str(new_id))
    logger.info(f"New ID, written in the file: {new_id}")
