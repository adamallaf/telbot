import os
import sys
import logger
from logging import getLogger
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from threading import Thread

from cmds import CMDS
from security import getUserByID
from security import owner_only
from utils import readToken
from utils import getToken


def main():
    logger = getLogger("Bot")
    logger.info("Starting telegram bot...")
    if readToken():
        logger.info("Token read successfully")
    updater = Updater(token=getToken())
    dispatcher = updater.dispatcher

    def stop():
        updater.stop()
        logger.info(f"{updater.bot.first_name} is stopped.")

    def stop_and_restart():
        logger.info(f"{updater.bot.first_name} is restarting...")
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    @owner_only
    def restart(bot, update):
        user_id = update.message.from_user.id
        user = getUserByID(user_id)
        logger.info(f"{user}: restart!")
        update.message.reply_text('Restarting...')
        Thread(target=stop_and_restart).start()

    @owner_only
    def shutdown(bot, update):
        user_id = update.message.from_user.id
        user = getUserByID(user_id)
        logger.info(f"{user}: shutdown !!!")
        update.message.reply_text('Shutting down...')
        Thread(target=stop).start()

    dispatcher.add_handler(CommandHandler('restart', restart))
    dispatcher.add_handler(CommandHandler('shutdown', shutdown))

    for cmd, handler in CMDS.items():
        dispatcher.add_handler(CommandHandler(cmd, handler, pass_args=True))

    logger.info(f"{updater.bot.first_name} is ready!")
    updater.start_polling()
    return 0


if __name__ == "__main__":
    sys.exit(main())
