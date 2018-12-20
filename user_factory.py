from users import Admin, Owner, User, UserBase, Unknown


class UserFactory:
    @staticmethod
    def createUser(user_entry: str) -> UserBase:
        _id, _p = user_entry.split(" ")
        _id = int(_id)
        if _p == 'U':
            return User(_id)
        if _p == 'A':
            return Admin(_id)
        if _p == 'O':
            return Owner(_id)
        if _p == 'x':
            return Unknown(_id)
        raise ValueError(f"Wrong user entry \"{user_entry}\"!")
