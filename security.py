

__white_list = []


def __loadWhiteList():
    global __white_list
    with open('user.wlist', 'r') as f:
        users = f.read()
    user_list = users.split("\n")
    __white_list = []
    for _uid in user_list:
        try:
            __white_list.append(int(_uid))
        except ValueError:
            pass
    print(__white_list)


def isAuthorized(user_id: int) -> bool:
    return user_id in __white_list


def addUser(user_id: int) -> bool:
    if isAuthorized(user_id):
        return False
    entry = "{}\n".format(user_id)
    with open('user.wlist', 'a') as f:
        f.write(entry)
    __loadWhiteList()
    return True


def removeUser(user_id: int) -> bool:
    if isAuthorized(user_id):
        __white_list.remove(user_id)
        with open('user.wlist', 'w') as f:
            for _user in __white_list:
                f.write("{}\n".format(_user))
        __loadWhiteList()
        return True
    return False


def getUsers() -> list:
    return __white_list[:]


__loadWhiteList()
