#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# https://www.uvicorn.org/settings/
export UVICORN_HOST="0.0.0.0"
export UVICORN_PORT=80

alembic upgrade head && uvicorn main:app --reload --host 0.0.0.0 --port 80 --proxy-headers

