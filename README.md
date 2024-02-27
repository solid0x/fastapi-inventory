# Inventory
An example of an asynchronous inventory FastAPI project with SQLAlchemy ORM, covered by tests. It includes integration and endpoint tests with stub injection.

## Endpoints
| Description       | Method | URL                | Request Body    |
|-------------------|--------|--------------------|-----------------|
| Get All Items     | GET    | `/items`           | None            |
| Get Item by ID    | GET    | `/items/{item_id}` | None            |
| Create Item       | POST   | `/items`           | `{ name: str }` |
| Delete Item by ID | DELETE | `/items/{item_id}` | None            |

Visit http://localhost:8000 to access the full API documentation.

## Getting Started
- Clone the repository
- Build and start the containers using Docker Compose:
```
docker-compose up --build
```
- Access the FastAPI application at http://localhost:8000