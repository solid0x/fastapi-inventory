from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from models import Item


class ItemStore:
    def __init__(self, async_session: async_sessionmaker[AsyncSession]):
        self.async_session = async_session

    async def get_item(self, item_id: int) -> Item | None:
        async with self.async_session() as session:
            statement = select(Item).where(Item.id == item_id)
            result = await session.execute(statement)
            return result.scalar()

    async def get_items(self) -> list[Item]:
        async with self.async_session() as session:
            statement = select(Item)
            result = await session.execute(statement)
            return list(result.scalars().all())

    async def create_item(self, name: str) -> Item:
        async with self.async_session() as session:
            item = Item(name=name)
            session.add(item)
            await session.commit()
            return item

    async def delete_item(self, item_id: int) -> Item | None:
        async with self.async_session() as session:
            statement = select(Item).where(Item.id == item_id)
            result = await session.execute(statement)
            item = result.scalar()
            if item:
                await session.delete(item)
                await session.commit()
                return item
