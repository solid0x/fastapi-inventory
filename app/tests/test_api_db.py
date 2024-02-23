import pytest
import pytest_asyncio
from httpx import AsyncClient

from db import async_session, init_db
from main import app
from store import ItemStore


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    await init_db(clean=True)
    item_store = ItemStore(async_session)
    await item_store.create_item("db_item 1")


@pytest.mark.asyncio
async def test_get_items():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(f"/items")

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_item():
    item_id = 1
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(f"/items/{item_id}")

    assert response.status_code == 200
    assert response.json() == {"id": item_id, "name": "db_item 1"}


@pytest.mark.asyncio
async def test_get_item_not_present():
    item_id = 2
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(f"/items/{item_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


@pytest.mark.asyncio
async def test_create_item():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(f"/items", json={"name": "db_item 2"})

    assert response.status_code == 200
    assert response.json() == {"id": 2, "name": "db_item 2"}
