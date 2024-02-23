export DATABASE_URL="sqlite+aiosqlite:///:memory:"
pytest -p no:cacheprovider --cov=src --cov-report=html