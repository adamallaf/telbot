from actions import send_action, ChatAction
from logger import printLog
from security import authorized
from security import addUser
from security import removeUser
from security import getUserByID
from security import getUsersIDs
from shell import Shell
from user_info import updateUsers

alarm = None #Alarm()
shell = {}


@updateUsers
@send_action(ChatAction.TYPING)
def startCmd(bot, update, args):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text="Hello!")


@updateUsers
@authorized
@send_action(ChatAction.TYPING)
def armCmd(bot, update, args):
    global alarm
    user_id = update.message.from_user.id
    user = getUserByID(user_id)
    chat_id = update.message.chat_id
    printLog(f"{user}: Arming!")
    alarm.arm()
    bot.send_message(chat_id=chat_id, text="Armed!")


@updateUsers
@authorized
@send_action(ChatAction.TYPING)
def disarmCmd(bot, update, args):
    global alarm
    user_id = update.message.from_user.id
    user = getUserByID(user_id)
    chat_id = update.message.chat_id
    printLog(f"{user}: Disarming!")
    alarm.disarm()
    bot.send_message(chat_id=chat_id, text="Disarmed!")


@updateUsers
@authorized
@send_action(ChatAction.TYPING)
def addUserCmd(bot, update, args):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    if not args:
        bot.send_message(chat_id=chat_id, text="Wrong command use!\nusage: /adduser <id>")
        return
    user = getUserByID(user_id)
    _arg = int(args.pop(0))
    printLog(f"{user}: Adding user {_arg}...")
    msg = f"User {_arg} already exists!"
    if addUser(_arg, "U"):
        msg = f"User {_arg} added!"
        printLog(msg)
    bot.send_message(chat_id=chat_id, text=msg)


@updateUsers
@authorized
@send_action(ChatAction.TYPING)
def removeUserCmd(bot, update, args):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    if not args:
        bot.send_message(chat_id=chat_id, text="Wrong command use!\nusage: /rmuser <id>")
        return
    user = getUserByID(user_id)
    _arg = int(args.pop(0))
    printLog(f"{user}: Removing user {_arg}...")
    msg = f"User {_arg} doesn\'t exists!"
    if removeUser(_arg):
        msg = f"User {_arg} removed!"
    printLog(msg)
    bot.send_message(chat_id=chat_id, text=msg)


@updateUsers
@authorized
@send_action(ChatAction.TYPING)
def getUsersCmd(bot, update, args):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    user = getUserByID(user_id)
    printLog(f"{user}: get user list")
    user_list = getUsersIDs()
    users = "{}".format("".join(f"{_uid}\n" for _uid in user_list))
    bot.send_message(chat_id=chat_id, text=users)


@updateUsers
@send_action(ChatAction.TYPING)
def printUserID(bot, update, args):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    user = getUserByID(user_id)
    printLog(f"{user}: what is my ID")
    bot.send_message(chat_id=chat_id, text=user_id)


@updateUsers
@authorized
@send_action(ChatAction.TYPING)
def printAvailableCmds(bot, update, args):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    user = getUserByID(user_id)
    printLog(f"{user}: print available commands")
    cmds = "{}".format("".join(f"{_cmd}\n" for _cmd in CMDS.keys()))
    bot.send_message(chat_id=chat_id, text=cmds)


@updateUsers
@authorized
@send_action(ChatAction.TYPING)
def execute(bot, update, args):
    global shell
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    if not args:
        bot.send_message(chat_id=chat_id, text="Wrong command use!\nusage: /exec <cmd>")
        return
    user = getUserByID(user_id)
    _args = " ".join(args)
    printLog(f"{user}: execute {_args}")
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
