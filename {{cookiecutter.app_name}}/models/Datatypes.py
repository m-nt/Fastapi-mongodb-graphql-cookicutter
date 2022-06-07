import strawberry


@strawberry.type
class User:
    username: str = ""
    password: str = ""
    email: str = ""
    full_name: str = ""
    token: str = ""

    def __init__(self, dict):
        self.__dict__ = dict

    @staticmethod
    def parse_obj(dict):
        return User(dict=dict)


@strawberry.input
class UserInput:
    username: str = ""
    password: str = ""
    email: str = ""
    full_name: str = ""
    token: str = ""
