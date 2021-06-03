import csv
import os
import tempfile
from pathlib import Path

import pytest

from ..handlers import SWAPIHandler
from ..types import Person
from .mock_data import people_mock, planets_mock

pytestmark = pytest.mark.django_db


def test_planets_map(requests_mock):
    requests_mock.get("https://swapi.dev/api/planets?page=1", text=planets_mock)
    handler = SWAPIHandler()
    assert len(handler.planets_name_map) == 10


def test_fetch_data(requests_mock, settings):
    """Example integration test"""
    requests_mock.get("https://swapi.dev/api/planets?page=1", text=planets_mock)
    requests_mock.get("https://swapi.dev/api/people?page=1", text=people_mock)

    with tempfile.TemporaryDirectory() as tmpdirname:
        settings.SWAPI_DATA_VAULT = Path(tmpdirname)
        handler = SWAPIHandler()
        handler.fetch_people("test_data")
        assert "test_data.csv" in os.listdir(tmpdirname)

        with open(str(handler.FINAL_FILE_PATH).format(filename="test_data")) as csvfile:
            reader = csv.DictReader(csvfile)
            assert set(reader.fieldnames) == set(Person.__annotations__.keys())
            assert len([i for i in reader]) == 10
