import os
import sys
from alarm import Alarm
from security import isAuthorized
from security import addUser
from security import removeUser
from security import getUsers


alarm = None #Alarm()


def startCmd(bot, update, args):
    bot.send_message(chat_id=update.message.chat_id, text="Hello!")


def armCmd(bot, update, args):
    global alarm
    user_id = update.message.from_user.id
    if not isAuthorized(user_id):
        return
    sys.stdout.write("{}: Arming!\n".format(user_id))
    alarm.arm()
    bot.send_message(chat_id=update.message.chat_id, text="Armed!")


def disarmCmd(bot, update, args):
    global alarm
    user_id = update.message.from_user.id
    if not isAuthorized(user_id):
        return
    sys.stdout.write("{}: Disarming!\n".format(user_id))
    alarm.disarm()
    bot.send_message(chat_id=update.message.chat_id, text="Disarmed!")


def addUserCmd(bot, update, args):
    user_id = update.message.from_user.id
    if not isAuthorized(user_id):
        return
    if not args:
        bot.send_message(chat_id=update.message.chat_id, text="Wrong command use!\nusage: /adduser <id>")
        return
    _arg = int(args.pop(0))
    sys.stdout.write("{}\n".format("Adding user {} to white list...".format(_arg)))
    msg = "User {} already exists!".format(_arg)
    if addUser(_arg):
        msg = "User {} added!".format(_arg)
        sys.stdout.write("{}\n".format(msg))
    bot.send_message(chat_id=update.message.chat_id, text=msg)


def removeUserCmd(bot, update, args):
    user_id = update.message.from_user.id
    if not isAuthorized(user_id):
        return
    if not args:
        bot.send_message(chat_id=update.message.chat_id, text="Wrong command use!\nusage: /rmuser <id>")
        return
    _arg = int(args.pop(0))
    sys.stdout.write("{}\n".format("Removing user {} from white list...".format(_arg)))
    msg = "User {} doesn\'t exists!".format(_arg)
    if removeUser(_arg):
        msg = "User {} removed!".format(_arg)
    sys.stdout.write("{}\n".format(msg))
    bot.send_message(chat_id=update.message.chat_id, text=msg)


def getUsersCmd(bot, update, args):
    user_id = update.message.from_user.id
    if not isAuthorized(user_id):
        return
    user_list = getUsers()
    users = "{}".format("".join("{}\n".format(_u) for _u in user_list))
    sys.stdout.write("{}: get user list\n".format(user_id))
    bot.send_message(chat_id=update.message.chat_id, text=users)


def printUserID(bot, update, args):
    user_id = update.message.from_user.id
    sys.stdout.write("{}: what my ID\n".format(user_id))
    bot.send_message(chat_id=update.message.chat_id, text=user_id)


CMDS = {
    'start': startCmd,
    #'arm': armCmd,
    #'disarm': disarmCmd,
    'adduser': addUserCmd,
    'rmuser': removeUserCmd,
    'users': getUsersCmd,
    'myid': printUserID,
}
