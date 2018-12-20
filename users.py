from user_base import UserBase, UserPermissions


class User(UserBase):
    def __init__(self, user_id):
        super().__init__(user_id, permissions=UserPermissions.USER)


class Admin(UserBase):
    def __init__(self, user_id):
        super().__init__(user_id, permissions=UserPermissions.ADMIN)


class Owner(UserBase):
    def __init__(self, user_id):
        super().__init__(user_id, permissions=UserPermissions.OWNER)


class Unknown(UserBase):
    def __init__(self, user_id):
        super().__init__(user_id, permissions=UserPermissions.Unknown)
