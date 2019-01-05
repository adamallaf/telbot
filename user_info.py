from functools import wraps
from pathlib import Path


__users = []


def updateUsers(func):
    @wraps(func)
    def command_func(*args, **kwargs):
        bot, update = args
        user = update.effective_user
        if user.id not in __users:
            __saveUserInfo(user)
            __users.append(user.id)
        return func(bot, update, **kwargs)

    return command_func


def __saveUserInfo(user):
    # example user attributes:
    # {'id': 0000000, 'first_name': 'FirstName', 'is_bot': False, 'last_name': 'LastName', 'username': 'UsErNaMe', 'language_code': 'en'}
    b = Path("user_accounts/")
    b.mkdir(exist_ok=True)
    p = b / Path(f"{user.id}")
    if not p.exists():
        output = f"username={user.username}\n"
        output += f"first_name={user.first_name}\n"
        output += f"last_name={user.last_name}\n"
        output += f"is_bot={user.is_bot}\n"
        output += f"language_code={user.language_code}\n"
        p.write_text(output)


def getAvailableUserInfoIDs() -> list:
    return __users


def getUserInfo(user_id) -> dict:
    return __readUserInfo(user_id)


def __readUserInfo(user_id: int) -> dict:
    b = Path("user_accounts/")
    b.mkdir(exist_ok=True)
    p = b / Path(f"{user_id}")
    result = {}
    if p.exists():
        result = {'id': user_id}
        info = p.read_text()
        for line in info.split('\n'):
            if line:
                k, v = line.split('=')
                if k == "is_bot":
                    result[k] = v == "True"
                else:
                    result[k] = v
    return result


def __loadUserInfoList():
    b = Path("user_accounts/")
    b.mkdir(exist_ok=True)
    __users.clear()
    for user_id in b.iterdir():
        __users.append(int(user_id.name))


__loadUserInfoList()
