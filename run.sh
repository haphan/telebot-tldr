#!/bin/bash
UVICORN_PORT="${PORT:-8080}"
poetry run uvicorn app:app --workers 1 --port $UVICORN_PORT --host 0.0.0.0