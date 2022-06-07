import strawberry
from typing import List
from models.Datatypes import *


@strawberry.type
class Schema:
    users: List[User]
