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
