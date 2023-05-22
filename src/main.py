import logging

from fastapi import FastAPI

from src.config import Config
from src.persistence.database import Database
from src.routers import root_router

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
app.include_router(root_router)


@app.on_event("startup")
async def startup():
    #   Connect to database
    await database.setup(
        f'postgresql+asyncpg://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.database}?client_encoding=utf8')
