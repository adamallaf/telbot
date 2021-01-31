import re
from functools import wraps
from logging import getLogger
from typing import List
from user_factory import UserFactory
from user_base import UserBase
from user_base import UserPermissions


__white_list = []
__entry_pattern = re.compile(r"^\d{6,16} [AOU]$", re.MULTILINE)
__logger = getLogger("security")


def __loadWhiteList():
    global __white_list
    global __logger
    __logger.info("Loading user list...")
    with open('user.wlist', 'r') as f:
        users = f.read()
    user_list = __entry_pattern.findall(users)
    __white_list = []
    for _user_entry in user_list:
        try:
            __white_list.append(UserFactory.createUser(_user_entry))
        except ValueError:
            pass
    __logger.info(f"user list loaded! {__white_list}")


def isAuthorized(user_id: int) -> bool:
    id_list = getUsersIDs()
    return user_id in id_list


def addUser(user_id: int, user_type: str) -> bool:
    if not isAuthorized(user_id):
        entry = f"{user_id} {user_type}"
        if __entry_pattern.findall(entry):
            __white_list.append(UserFactory.createUser(entry))
            with open('user.wlist', 'a') as f:
                f.write(f"{entry}\n")
            return True
    return False


def removeUser(user_id: int) -> bool:
    if isAuthorized(user_id):
        for user in __white_list:
            if user_id == user.id:
                __white_list.remove(user)
        entry_pattern = re.compile(f"^{user_id} [AOU]$\n", re.MULTILINE)
        with open('user.wlist', 'r') as f:
            entries = f.read()
            x = entry_pattern.findall(entries)
            if x:
                entries = entries.replace(x[0], '')
        with open('user.wlist', 'w') as f:
            for entry in entries.split("\n"):
                if entry:
                    f.write(f"{entry}\n")
        return True
    return False


def getUserByID(user_id: int) -> UserBase:
    if isAuthorized(user_id):
        for user in getUsers():
            if user_id == user.id:
                return user
    return UserFactory.createUser(f"{user_id} x")


def getUsers() -> List[UserBase]:
    return __white_list[:]


def getUsersIDs() -> List[int]:
    return [user.id for user in __white_list]


def authorized(func):
    global __logger

    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        user = getUserByID(user_id)
        if not isAuthorized(user_id):
            __logger.warning(f"{user}: tried authorized command \"{update.message.text}\" !!")
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def owner_only(func):
    global __looger

    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        user = getUserByID(user_id)
        if user.permissions != UserPermissions.OWNER:
            __logger.warning(f"{user}: tried restricted command \"{update.message.text}\" !!")
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


__loadWhiteList()
