set -x && isort . && black . && mypy . && flake8 .