import os
import sys
from alarm import Alarm
from security import isAuthorized
from security import addUser
from security import removeUser
from security import getUsers
from shell import Shell


alarm = None #Alarm()
shell = {}


def startCmd(bot, update, args):
    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id=chat_id, action='typing')
    bot.send_message(chat_id=chat_id, text="Hello!")


def armCmd(bot, update, args):
    global alarm
    user_id = update.message.from_user.id
    if not isAuthorized(user_id):
        return
    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id=chat_id, action='typing')
    sys.stdout.write("{}: Arming!\n".format(user_id))
    alarm.arm()
    bot.send_message(chat_id=chat_id, text="Armed!")


def disarmCmd(bot, update, args):
    global alarm
    user_id = update.message.from_user.id
    if not isAuthorized(user_id):
        return
    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id=chat_id, action='typing')
    sys.stdout.write("{}: Disarming!\n".format(user_id))
    alarm.disarm()
    bot.send_message(chat_id=chat_id, text="Disarmed!")


def addUserCmd(bot, update, args):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    if not isAuthorized(user_id):
        return
    if not args:
        bot.send_message(chat_id=chat_id, text="Wrong command use!\nusage: /adduser <id>")
        return
    bot.send_chat_action(chat_id=chat_id, action='typing')
    _arg = int(args.pop(0))
    sys.stdout.write("{}\n".format("Adding user {} to white list...".format(_arg)))
    msg = "User {} already exists!".format(_arg)
    if addUser(_arg):
        msg = "User {} added!".format(_arg)
        sys.stdout.write("{}\n".format(msg))
    bot.send_message(chat_id=chat_id, text=msg)


def removeUserCmd(bot, update, args):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    if not isAuthorized(user_id):
        return
    if not args:
        bot.send_message(chat_id=chat_id, text="Wrong command use!\nusage: /rmuser <id>")
        return
    bot.send_chat_action(chat_id=chat_id, action='typing')
    _arg = int(args.pop(0))
    sys.stdout.write("{}\n".format("Removing user {} from white list...".format(_arg)))
    msg = "User {} doesn\'t exists!".format(_arg)
    if removeUser(_arg):
        msg = "User {} removed!".format(_arg)
    sys.stdout.write("{}\n".format(msg))
    bot.send_message(chat_id=chat_id, text=msg)


def getUsersCmd(bot, update, args):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    if not isAuthorized(user_id):
        return
    bot.send_chat_action(chat_id=chat_id, action='typing')
    sys.stdout.write("{}: get user list\n".format(user_id))
    user_list = getUsers()
    users = "{}".format("".join("{}\n".format(_u) for _u in user_list))
    bot.send_message(chat_id=chat_id, text=users)


def printUserID(bot, update, args):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id=chat_id, action='typing')
    sys.stdout.write("{}: what my ID\n".format(user_id))
    bot.send_message(chat_id=chat_id, text=user_id)


def printAvailableCmds(bot, update, args):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    if not isAuthorized(user_id):
        return
    bot.send_chat_action(chat_id=chat_id, action='typing')
    sys.stdout.write("{}: print available commands\n".format(user_id))
    cmds = "{}".format("".join(f"{_cmd}\n" for _cmd in CMDS.keys()))
    bot.send_message(chat_id=chat_id, text=cmds)


def execute(bot, update, args):
    global shell
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    if not isAuthorized(user_id):
        return
    if not args:
        bot.send_message(chat_id=chat_id, text="Wrong command use!\nusage: /exec <cmd>")
        return
    bot.send_chat_action(chat_id=chat_id, action='typing')
    _args = " ".join(args)
    sys.stdout.write("{}: execute {}\n".format(user_id, _args))
    if user_id not in shell.keys():
        shell[user_id] = Shell()
    result = shell[user_id].execute(_args)
    bot.send_message(chat_id=chat_id, text=result)


CMDS = {
    'start': startCmd,
    #'arm': armCmd,
    #'disarm': disarmCmd,
    'adduser': addUserCmd,
    'rmuser': removeUserCmd,
    'users': getUsersCmd,
    'myid': printUserID,
    'help': printAvailableCmds,
    'exec': execute,
}
