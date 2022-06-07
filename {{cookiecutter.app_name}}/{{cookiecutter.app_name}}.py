import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import dotenv
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from models.Datatypes import *
from models.Schemas import *
from tools.resolvers import *

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "{{cookiecutter.secret_key}}"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


dotenv.load_dotenv()


@strawberry.type
class Query:
    results: Schema = strawberry.field(resolver=get_users)
    echo: Union[str, None] = strawberry.field(resolver=echo)
    pass


@strawberry.type
class Mutaion:
    add_user: User = strawberry.field(resolver=add_user)
    pass


schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
