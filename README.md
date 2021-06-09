# Welcome

## How to use:

1. `docker-compose build`
2. `docker-compose up`

As `swapi.co` is no longer alive, `swapi.dev` is used as replacement - configurable via settings.

Default admin credentials can be set via `DEFAULT_SUPERUSER_USERNAME` and `DEFAULT_SUPERUSER_PASSWORD`
ENV params (set them inside `.env` file). The default values are `admin` and `admin`.

TODO:

1. Use celery - fetching data should be a task
2. Use DRF to create REST API instead of html-based views. Maybe even use FastAPI instead of Django.
3. Add more tests
4. Better UI
5. There are some additional `TODO` tags within the code.

I'll gladly discuss any plans for extending this app.
