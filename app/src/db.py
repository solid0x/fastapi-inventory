from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from models import Base
from settings import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def init_db(clean=False):
    async with engine.begin() as conn:
        if clean:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
