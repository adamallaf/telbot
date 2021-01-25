import time
from pathlib import Path

from alarm import Alarm
from actions import send_action, ChatAction
from logging import getLogger
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
from cam0 import cam0_take_shot


#alarm = Alarm()
shell = {}


@updateUsers
@send_action(ChatAction.TYPING)
def startCmd(bot, update, args):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    getLogger("startCmd").info("{} called /start".format(user_id))
    bot.send_message(chat_id=chat_id, text="Hello!")


@updateUsers
@authorized
@send_action(ChatAction.TYPING)
def armCmd(bot, update, args):
    global alarm
    user_id = update.message.from_user.id
    user = getUserByID(user_id)
    chat_id = update.message.chat_id
    getLogger("armCmd").info(f"{user}: Arming!")
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
    getLogger("disarmCmd").info(f"{user}: Disarming!")
    alarm.disarm()
    bot.send_message(chat_id=chat_id, text="Disarmed!")


@updateUsers
@authorized
@send_action(ChatAction.TYPING)
def addUserCmd(bot, update, args):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    logger = getLogger("addUserCmd")
    if not args:
        bot.send_message(chat_id=chat_id, text="Wrong command use!\nusage: /adduser <id>")
        return
    user = getUserByID(user_id)
    _arg = int(args.pop(0))
    logger.info(f"{user}: Adding user {_arg}...")
    msg = f"User {_arg} already exists!"
    if addUser(_arg, "U"):
        msg = f"User {_arg} added!"
        logger.info(msg)
    bot.send_message(chat_id=chat_id, text=msg)


@updateUsers
@authorized
@send_action(ChatAction.TYPING)
def removeUserCmd(bot, update, args):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    logger = getLogger("removeUserCmd")
    if not args:
        bot.send_message(chat_id=chat_id, text="Wrong command use!\nusage: /rmuser <id>")
        return
    user = getUserByID(user_id)
    _arg = int(args.pop(0))
    logger.info(f"{user}: Removing user {_arg}...")
    msg = f"User {_arg} doesn\'t exists!"
    if removeUser(_arg):
        msg = f"User {_arg} removed!"
    logger.info(msg)
    bot.send_message(chat_id=chat_id, text=msg)


@updateUsers
@authorized
@send_action(ChatAction.TYPING)
def getUsersCmd(bot, update, args):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    user = getUserByID(user_id)
    logger = getLogger("getUsersCmd")
    logger.info(f"{user}: get user list")
    user_list = getUsersIDs()
    users = "{}".format("".join(f"{_uid}\n" for _uid in user_list))
    bot.send_message(chat_id=chat_id, text=users)


@updateUsers
@send_action(ChatAction.TYPING)
def printUserID(bot, update, args):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    user = getUserByID(user_id)
    getLogger("printUserID").info(f"{user}: what is my ID?")
    bot.send_message(chat_id=chat_id, text=user_id)


@updateUsers
@authorized
@send_action(ChatAction.TYPING)
def printAvailableCmds(bot, update, args):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    user = getUserByID(user_id)
    getLogger("printAvailableCmds").info(f"{user}: print available commands")
    cmds = "{}".format("".join(f"{_cmd}\n" for _cmd in CMDS.keys()))
    bot.send_message(chat_id=chat_id, text=cmds)


@updateUsers
@owner_only
@send_action(ChatAction.TYPING)
def execute(bot, update, args):
    global shell
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    logger = getLogger("execute")
    if not args:
        bot.send_message(chat_id=chat_id, text="Wrong command use!\nusage: /exec <cmd>")
        return
    user = getUserByID(user_id)
    _args = " ".join(args)
    logger.info(f"{user}: execute {_args}")
    if user_id not in shell.keys():
        shell[user_id] = Shell()
    result = shell[user_id].execute(_args)
    logger.info(result)
    bot.send_message(chat_id=chat_id, text=result)


@updateUsers
@owner_only
@send_action(ChatAction.TYPING)
def userInfoCmd(bot, update, args):
    user_id = update.message.from_user.id
    user = getUserByID(user_id)
    chat_id = update.message.chat_id
    logger = getLogger("userInfoCmd")
    result = ""
    logger.info(f"{user}: user info {' '.join(args)}")
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
    logger.info("result:\n{}".format(result))
    bot.send_message(chat_id=chat_id, text=result)


@updateUsers
@owner_only
@send_action(ChatAction.TYPING)
def getFileCmd(bot, update, args):
    user_id = update.message.from_user.id
    user = getUserByID(user_id)
    chat_id = update.message.chat_id
    logger = getLogger("getFileCmd")
    if not args:
        bot.send_message(chat_id=chat_id, text="Wrong command use!\nusage: /getfile <file_path>")
        return
    _arg = args.pop(0)
    p = Path(_arg)
    logger.info(f"{user}: get file {_arg}")
    if p.exists():
        if p.is_file():
            logger.info("Sending file \"{}\"...".format(_arg))
            bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_DOCUMENT)
            bot.send_document(chat_id=chat_id, document=open(_arg, 'rb'), timeout=600)
        else:
            _msg = f"\"{_arg}\" is not a file!"
            logger.info(_msg)
            bot.send_message(chat_id=chat_id, text=_msg)
    else:
        _msg = f"File \"{_arg}\" not found!"
        logger.info(_msg)
        bot.send_message(chat_id=chat_id, text=_msg)


@updateUsers
@authorized
@send_action(ChatAction.TYPING)
def getMeteoCmd(bot, update, args):
    user_id = update.message.from_user.id
    user = getUserByID(user_id)
    chat_id = update.message.chat_id
    logger = getLogger("getMeteoCmd")
    p = Path("./meteo.png")
    logger.info(f"{user}: get meteo")
    if p.exists():
        if time.time() - p.stat().st_ctime < 3600:
            logger.info("sending cached meteo chart")
            bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_PHOTO)
            bot.send_photo(chat_id=chat_id, photo=p.open('rb'), timeout=600)
            return
    if get_meteo():
        logger.info(f"{p.name} updated!")
        if p.exists():
            logger.info("sending file")
            bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_PHOTO)
            bot.send_photo(chat_id=chat_id, photo=p.open('rb'), timeout=600)
        else:
            _msg = f"{p.name} was not saved!"
            logger.error(_msg)
            bot.send_message(chat_id=chat_id, text=_msg)
    else:
        bot.send_message(chat_id=chat_id, text="Could not get meteo info!")
        logger.error(f"Could not download {p.name}!")


@updateUsers
@authorized
@send_action(ChatAction.TYPING)
def cam0ShotCmd(bot, update, args):
    user_id = update.message.from_user.id
    user = getUserByID(user_id)
    chat_id = update.message.chat_id
    logger = getLogger("cam0ShotCmd")
    p = Path("./photo_cam0.jpg")
    logger.info(f"{user}: cam0 shot")
    if p.exists():
        if time.time() - p.stat().st_ctime < 2:
            logger.info("sending cached file")
            bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_PHOTO)
            bot.send_photo(chat_id=chat_id, photo=p.open('rb'), timeout=600)
            return
    if cam0_take_shot():
        logger.info(f"{p.name} updated!")
        if p.exists():
            logger.info("sending file")
            bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_PHOTO)
            bot.send_photo(chat_id=chat_id, photo=p.open('rb'), timeout=600)
        else:
            _msg = f"{p.name} was not saved!"
            logger.error(_msg)
            bot.send_message(chat_id=chat_id, text=_msg)

    else:
        _msg = "Could not take photo on cam 0!"
        logger.error(_msg)
        bot.send_message(chat_id=chat_id, text=_msg)


CMDS = {
    'start': startCmd,
#    'arm': armCmd,
#    'disarm': disarmCmd,
    'adduser': addUserCmd,
    'rmuser': removeUserCmd,
    'users': getUsersCmd,
    'myid': printUserID,
    'help': printAvailableCmds,
    'exec': execute,
    'userinfo': userInfoCmd,
    'getfile': getFileCmd,
    'meteo': getMeteoCmd,
    'cam0_shot': cam0ShotCmd,
}
