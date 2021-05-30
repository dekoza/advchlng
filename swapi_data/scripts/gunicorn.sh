#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

python manage.py migrate
python manage.py collectstatic --noinput --verbosity 0
gunicorn config.asgi --bind :8000 --chdir=/app -k uvicorn.workers.UvicornWorker
