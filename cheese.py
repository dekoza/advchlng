#!env python
# – Red Windsor?
# – Normally, sir, yes, but today the van broke down.

import os
import pathlib

import typer

run = os.system
app = typer.Typer()


@app.command()
def bootstrap():
    """
    Prepare project directory for local development.
    """
    if not pathlib.Path(".env").exists():
        typer.echo("Please edit .env file")  # TODO: run cookiecutter-like questionnaire
    run("poetry run pre-commit install")


@app.command("up", hidden=True)
@app.command()
def launch():
    """
    Run local server. Shortcut: up
    """
    run("docker-compose up --build")


@app.command("t", hidden=True)
@app.command()
def test():
    """
    Run tests suite. Shortcut: t
    """
    run("docker-compose run django python manage.py test")


@app.command()
def bash():
    """
    Run bash inside docker.
    """
    run("docker-compose exec django bash")


@app.command("sh", hidden=True)
@app.command()
def shell():
    """
    Run backend shell inside docker. Shortcut: sh
    """
    run("docker-compose run django python manage.py shell_plus")


@app.command()
def clean():
    """
    Remove .pyc files.
    """
    run("docker-compose run django python manage.py clean_pyc")


@app.command()
def update():
    """
    Install and update new dependencies on already build image
    """
    run("docker-compose run django poetry install")


@app.command()
def collect():
    """
    Run collectstatic.
    """
    run("docker-compose run django python manage.py collectstatic --noinput")


@app.command("mm", hidden=True)
@app.command()
def migrations():
    """
    Create new migrations. Shortcut: mm
    """
    run("docker-compose run django python manage.py makemigrations")


@app.command("m", hidden=True)
@app.command()
def migrate():
    """
    Apply migrations. Shortcut: m
    """
    run("docker-compose run django python manage.py migrate")


if __name__ == "__main__":
    app()
