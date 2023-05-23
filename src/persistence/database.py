import logging
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from src.config import Config
from src.persistence.models.base_models import BaseModel
from src.persistence.models.user_model import UserModel

"""
This class is a singleton that manages the database connection.
It is created when the app starts and destroyed when the app stops.
"""


class Database:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Database()
        return cls._instance

    def __init__(self):
        if Database._instance is not None:
            raise Exception("This class is a singleton!")
        self._logger = logging.getLogger(__name__)
        self._config = Config.get_instance()
        self.engine = create_async_engine(f'postgresql+asyncpg://'
                                          f'{self._config.db.user}:{self._config.db.password}@{self._config.db.host}/'
                                          f'{self._config.db.database}')
        self.async_session_maker = async_sessionmaker(self.engine, expire_on_commit=False)


database = Database.get_instance()


async def create_db_and_tables():
    async with database.engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with database.async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, UserModel)
