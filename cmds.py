import time
from pathlib import Path

from actions import send_action, ChatAction
from logger import printLog
from meteo import get_meteo
from security import authorized
from security import addUser
from security import owner_only
from security import removeUser
from security import getUserByID
from security import getUsersIDs
from shell import Shell
from user_info import updateUsers
from user_info import getAvailableUserInfoIDs
from user_info import getUserInfo


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
@owner_only
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


@updateUsers
@owner_only
@send_action(ChatAction.TYPING)
def userInfoCmd(bot, update, args):
    user_id = update.message.from_user.id
    user = getUserByID(user_id)
    chat_id = update.message.chat_id
    result = ""
    printLog(f"{user}: user info {' '.join(args)}")
    if args:
        found = 0
        counter = 0
        if "all" in args:
            user_id_list = getAvailableUserInfoIDs()
            result = f"Found {len(user_id_list)} user's info:\n\n"
        else:
            user_id_list = [int(_arg) for _arg in args if _arg.isnumeric()]
        for uid in user_id_list:
            counter += 1
            output = getUserInfo(uid)
            if not output:
                result += f"{uid} - not found\n"
            else:
                found += 1
                result += f"{output['username']}({output['id']}) {'[Bot]' if output['is_bot'] else ''}\n"
                result += f"{output['first_name']} {output['last_name']}\n"
            if counter < len(user_id_list):
                result += 20 * "-" + "\n"
        if found < len(user_id_list):
            result = f"Found {found}/{len(user_id_list)} user's info:\n\n" + result
    else:
        user_id_list = getAvailableUserInfoIDs()
        result = f"{len(user_id_list)} user info available:\n\n"
        for uid in user_id_list:
            result += f"{uid}\n"
    bot.send_message(chat_id=chat_id, text=result)


@updateUsers
@owner_only
@send_action(ChatAction.TYPING)
def getFileCmd(bot, update, args):
    user_id = update.message.from_user.id
    user = getUserByID(user_id)
    chat_id = update.message.chat_id
    if not args:
        bot.send_message(chat_id=chat_id, text="Wrong command use!\nusage: /getfile <file_path>")
        return
    _arg = args.pop(0)
    p = Path(_arg)
    printLog(f"{user}: get file {_arg}")
    if p.exists():
        if p.is_file():
            bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_DOCUMENT)
            bot.send_document(chat_id=chat_id, document=open(_arg, 'rb'), timeout=600)
        else:
            bot.send_message(chat_id=chat_id, text=f"\"{_arg}\" is not a file!")
    else:
        bot.send_message(chat_id=chat_id, text=f"File \"{_arg}\" not found!")


@updateUsers
@owner_only
@send_action(ChatAction.TYPING)
def getMeteoCmd(bot, update, args):
    user_id = update.message.from_user.id
    user = getUserByID(user_id)
    chat_id = update.message.chat_id
    p = Path("./meteo.png")
    printLog(f"{user}: get meteo")
    if p.exists():
        if time.time() - p.stat().st_ctime < 3600:
            bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_PHOTO)
            bot.send_photo(chat_id=chat_id, photo=p.open('rb'), timeout=600)
            return
    if get_meteo():
        printLog(" * meteo.png updated!")
        if p.exists():
            bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_PHOTO)
            bot.send_photo(chat_id=chat_id, photo=p.open('rb'), timeout=600)
        else:
            bot.send_message(chat_id=chat_id, text="Meteo image was not saved!")
    else:
        bot.send_message(chat_id=chat_id, text="Could not get meteo info!")
        printLog(" X Could not download meteo.png!")


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
    'userinfo': userInfoCmd,
    'getfile': getFileCmd,
    'meteo': getMeteoCmd,
}
