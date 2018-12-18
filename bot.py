import sys
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters


from cmds import CMDS
from utils import readToken
from utils import getToken


def main():
    if readToken():
        sys.stdout.write("Token: {}\n".format(getToken()))
    updater = Updater(token=getToken())
    dispatcher = updater.dispatcher

    for cmd, handler in CMDS.items():
        dispatcher.add_handler(CommandHandler(cmd, handler, pass_args=True))

    updater.start_polling()
    return 0


if __name__ == "__main__":
    sys.exit(main())
