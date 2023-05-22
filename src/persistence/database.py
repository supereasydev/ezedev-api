import logging

from gino import Gino
from gino.schema import GinoSchemaVisitor

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
        self.db = Gino()
        self._logger = logging.getLogger(__name__)

    async def shutdown(self):
        bind = self.db.pop_bind()
        if bind:
            self._logger.info("Close PostgreSQL Connection")
            await bind.close()

    async def setup(self, uri):
        self._logger.info("Setup PostgreSQL connection")
        logging.getLogger('gino.engine._SAEngine').setLevel(logging.ERROR)
        await self.db.set_bind(uri)

        # Create tables
        self.db.gino: GinoSchemaVisitor
        # await db.gino.drop_all()  # Drop the db
        await self.db.gino.create_all()
        self._logger.info('Database tables created')
