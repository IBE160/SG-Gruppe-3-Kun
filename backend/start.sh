#!/bin/bash
set -euxo pipefail

poetry install --no-root --no-interaction --no-ansi

# Start the Uvicorn server
poetry run uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
