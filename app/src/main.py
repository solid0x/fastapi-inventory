from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException

from db import db
from schemas import CreateItemSchema, ItemNotFoundSchema, ItemSchema
from store import ItemStore
from utils import to_schema, to_schemas


@asynccontextmanager
async def lifespan(_: FastAPI):
    await db.create_database()
    yield


app = FastAPI(lifespan=lifespan)


def get_item_store() -> ItemStore:
    return ItemStore(db.async_session)


@app.get("/items")
async def get_items(
    item_store: ItemStore = Depends(get_item_store),
) -> list[ItemSchema]:
    items = await item_store.get_items()
    return to_schemas(items, ItemSchema)


@app.get("/items/{item_id}", responses={404: {"model": ItemNotFoundSchema}})
async def get_item(
    item_id: int, item_store: ItemStore = Depends(get_item_store)
) -> ItemSchema:
    item = await item_store.get_item(item_id)
    if not item:
        raise HTTPException(404, "Item not found")

    return to_schema(item, ItemSchema)


@app.post("/items")
async def create_item(
    item_schema: CreateItemSchema, item_store: ItemStore = Depends(get_item_store)
) -> ItemSchema:
    item = await item_store.create_item(item_schema.name)
    return to_schema(item, ItemSchema)


@app.delete("/items/{item_id}", responses={404: {"model": ItemNotFoundSchema}})
async def delete_item(
    item_id: int, item_store: ItemStore = Depends(get_item_store)
) -> ItemSchema:
    item = await item_store.delete_item(item_id)
    if not item:
        raise HTTPException(404, "Item not found")

    return to_schema(item, ItemSchema)
