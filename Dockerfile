FROM python:3.9.5

# python envs
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# python dependencies
COPY ./poetry.lock /
COPY ./pyproject.toml /
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# upload scripts
COPY ./swapi_data/scripts/entrypoint.sh ./swapi_data/scripts/start.sh ./swapi_data/scripts/gunicorn.sh ./swapi_data/scripts/wait-for-it.sh /
COPY ./swapi_data /app

WORKDIR /app
ENTRYPOINT ["/entrypoint.sh"]
CMD ["/gunicorn.sh"]
