import logging

from fastapi import FastAPI, HTTPException

from src.config import Config
from src.exceptions.unicorn_exception import UnicornException
from src.persistence.database import Database, create_db_and_tables
from src.routers import root_router
from src.routers.exception_handler import unicorn_error, HTTPException_error

logging.basicConfig(
    level=logging.INFO,
    format=u'%(levelname)-8s %(name)s:%(lineno)d [%(asctime)s] - %(message)s',
    # filename='back.log'
)

# Application initialization
app = FastAPI(
    title="eze dev",
    description=" eze dev REST API",
    version="0.1.0",
    docs_url="/",
    redoc_url=None,
    openapi_url="/openapi.json",
)

database = Database.get_instance()
config = Config.get_instance('.env')

# Register routers
app.add_exception_handler(UnicornException, unicorn_error)
app.add_exception_handler(HTTPException, HTTPException_error)
app.include_router(root_router)


@app.on_event("startup")
async def startup():
    #   Connect to database
    await create_db_and_tables()
