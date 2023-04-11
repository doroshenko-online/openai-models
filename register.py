import os
from databases import Database


class SingletonDatabase:
    database_url = None
    _instance = None
    _database = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.database_url = os.getenv("PSQL")
            cls._database = Database(cls.database_url)
        return cls._instance

    @property
    def database(self):
        return self._database

    async def connect(self):
        if not self._database.is_connected:
            await self._database.connect()

    async def disconnect(self):
        if self._database.is_connected:
            await self._database.disconnect()
