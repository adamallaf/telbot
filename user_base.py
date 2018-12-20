from enum import IntEnum


class UserPermissions(IntEnum):  # for now let it be like this
    USER = 1
    ADMIN = 2
    OWNER = 3


class UserBase:
    def __init__(self, user_id, permissions):
        self.__user_id = user_id
        self.__user_permissions = permissions

    @property
    def id(self) -> int:
        return self.__user_id

    @property
    def permissions(self) -> UserPermissions:
        return self.__user_permissions

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {self.__user_id}>"

    def __repr__(self):
        return self.__str__()
