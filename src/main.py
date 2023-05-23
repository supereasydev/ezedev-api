import logging

from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from src.config import Config
from src.exceptions.unicorn_exception import UnicornException
from src.persistence.database import Database, create_db_and_tables
from src.persistence.models.user_model import UserModel
from src.routers import root_router
from src.routers.exception_handler import unicorn_error
from src.security.configuration import auth_backend
from src.security.schemas import UserRead, UserCreate
from src.security.user_manager import get_user_manager

logging.basicConfig(
    level=logging.INFO,
    format=u'%(levelname)-8s %(name)s:%(lineno)d [%(asctime)s] - %(message)s',
    # filename='back.log'
)

# Application initialization
app = FastAPI(
    title="Изи Dev",
    description="Rest API для бэкэнд сервиса \"EZEDEV\"",
    version="0.1.0",
    docs_url="/",
    redoc_url=None,
    openapi_url="/openapi.json",
)

database = Database.get_instance()
config = Config.get_instance('.env')

# Register routers
app.add_exception_handler(UnicornException, unicorn_error)
app.include_router(root_router)

# Register authorization routes
fastapi_users = FastAPIUsers[UserModel, int](
    get_user_manager,
    [auth_backend],
)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="",
)


@app.on_event("startup")
async def startup():
    #   Connect to database
    await create_db_and_tables()
