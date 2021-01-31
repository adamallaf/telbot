import sys
from logging import getLogger

from bot import BotApp


def main():
    logger = getLogger("main")

    try:
        from config import config
        logger.info("Config loaded successfuly")
    except Exception as e:
        logger.error("Could not load config! {}".format(e))
        return 1

    BotApp(config).start()
    return 0


if __name__ == "__main__":
    sys.exit(main())
