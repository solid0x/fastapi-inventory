from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from models import Base
from settings import settings


class Database:
    def __init__(self):
        self.engine = create_async_engine(settings.DATABASE_URL, echo=True)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def create_database(self, clean=False):
        async with self.engine.begin() as conn:
            if clean:
                await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


db = Database()
