from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException

from db import async_session, init_db
from schemas import ItemSchema
from store import ItemStore
from utils import to_schema, to_schemas

app = FastAPI()


def get_item_store() -> ItemStore:
    return ItemStore(async_session)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


@app.get("/items")
async def get_items(
    item_store: ItemStore = Depends(get_item_store),
) -> list[ItemSchema]:
    items = await item_store.get_items()
    return to_schemas(items, ItemSchema)


@app.get("/items/{item_id}")
async def get_item(
    item_id: int, item_store: ItemStore = Depends(get_item_store)
) -> ItemSchema:
    item = await item_store.get_item(item_id)
    if not item:
        raise HTTPException(404, "Item not found")

    return to_schema(item, ItemSchema)


@app.post("/items")
async def create_item(
    item_schema: ItemSchema, item_store: ItemStore = Depends(get_item_store)
) -> ItemSchema:
    item = await item_store.create_item(item_schema.name)
    return to_schema(item, ItemSchema)


@app.delete("/items/{item_id}")
async def delete_item(
    item_id: int, item_store: ItemStore = Depends(get_item_store)
) -> ItemSchema:
    item = await item_store.delete_item(item_id)
    if not item:
        raise HTTPException(404, "Item not found")

    return to_schema(item, ItemSchema)
