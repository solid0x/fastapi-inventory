import pytest
import pytest_asyncio
from httpx import AsyncClient

from main import app, get_item_store

from .stub_store import StubItemStore


def get_test_item_store():
    return StubItemStore()


@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_stub():
    app.dependency_overrides[get_item_store] = get_test_item_store


@pytest.mark.asyncio
async def test_get_items():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/items")

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_item():
    item_id = 1
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(f"/items/{item_id}")

    assert response.status_code == 200
    assert response.json() == {"id": item_id, "name": "stub_item 1"}


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
        response = await client.post("/items", json={"name": "stub_item 2"})

    assert response.status_code == 200
    assert response.json() == {"id": 2, "name": "stub_item 2"}


@pytest.mark.asyncio
async def test_delete_item():
    async with AsyncClient(app=app, base_url="http://test") as client:
        delete_response = await client.delete("/items/1")

    assert delete_response.status_code == 200
    assert delete_response.json() == {"id": 1, "name": "stub_item 1"}


@pytest.mark.asyncio
async def test_delete_item_not_present():
    async with AsyncClient(app=app, base_url="http://test") as client:
        delete_response = await client.delete("/items/2")

    assert delete_response.status_code == 404
    assert delete_response.json() == {"detail": "Item not found"}
