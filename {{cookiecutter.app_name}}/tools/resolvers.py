from typing import List, Union
import motor.motor_asyncio
import os
from fastapi.encoders import jsonable_encoder
from models.Schemas import *
from models.Datatypes import *

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))
db = client["{{cookiecutter.app_name}}"]


async def get_users():
    result = await db["schemas"].find().to_list(length=10)
    users: List[User] = []
    for document in result:
        users.append(User(dict=document))
    return Schema(users=users)


async def add_user(user: UserInput) -> User:
    data = jsonable_encoder(user)
    user = await db["schemas"].find_one(
        {"$or": [{"username": user.username}, {"email": user.email}]}
    )
    if user:
        return User({})
    insert = await db["schemas"].insert_one(data)
    result = await db["schemas"].find_one({"_id": insert.inserted_id})
    if result:
        return User.parse_obj(result)
    return User({})


def echo(self, echo: Union[str, None] = "") -> str:
    return echo
