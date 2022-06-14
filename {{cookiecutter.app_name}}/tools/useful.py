from passlib.context import CryptContext
from jose import JWTError, jwt
import time
import motor

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "{{cookiecutter.secret_key}}"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def check_if_loggin(
    client: motor.motor_asyncio.AsyncIOMotorClient, token: str
) -> bool:
    db = client["twatter"]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        expire: int = payload.get("exp")
        if username is None or expire is None:
            return False
    except JWTError:
        return False
    if expire - time.time() <= 0:
        return False
    user_instant = await db["users"].find_one({"username": username})
    if user_instant is None:
        return False
    return True


def verify_password(pwd_context: CryptContext, plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(pwd_context: CryptContext, password):
    return pwd_context.hash(password)
