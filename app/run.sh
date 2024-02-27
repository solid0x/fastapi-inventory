export DATABASE_URL="postgresql+asyncpg://postgres:admin@localhost/inventory"
uvicorn --app-dir "./src" main:app --reload