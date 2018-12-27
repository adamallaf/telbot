import os
import sys
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from threading import Thread

from cmds import CMDS
from security import getUserByID
from security import isAuthorized
from user_base import UserPermissions
from utils import readToken
from utils import getToken


def main():
    if readToken():
        sys.stdout.write("Token: {}\n".format(getToken()))
    updater = Updater(token=getToken())
    dispatcher = updater.dispatcher

    def stop():
        updater.stop()

    def stop_and_restart():
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def restart(bot, update):
        user_id = update.message.from_user.id
        if not isAuthorized(user_id):
            return
        if getUserByID(user_id).permissions != UserPermissions.OWNER:
            return
        update.message.reply_text('Bot is restarting...')
        Thread(target=stop_and_restart).start()

    def shutdown(bot, update):
        user_id = update.message.from_user.id
        if not isAuthorized(user_id):
            return
        if getUserByID(user_id).permissions != UserPermissions.OWNER:
            return
        update.message.reply_text('Bot is shutting down...')
        Thread(target=stop).start()

    dispatcher.add_handler(CommandHandler('restart', restart))
    dispatcher.add_handler(CommandHandler('shutdown', shutdown))

    for cmd, handler in CMDS.items():
        dispatcher.add_handler(CommandHandler(cmd, handler, pass_args=True))

    updater.start_polling()
    return 0


if __name__ == "__main__":
    sys.exit(main())
