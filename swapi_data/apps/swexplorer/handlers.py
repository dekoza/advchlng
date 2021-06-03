import logging
import os
from pathlib import Path
from typing import Generator, Mapping, Optional, Union
from urllib.parse import urljoin
from uuid import uuid4

import jsonlines
import pendulum
import petl as etl
import requests
from apps.swexplorer.models import SwapiCollection
from apps.swexplorer.types import Person, RawPerson
from django.conf import settings
from django.utils.functional import cached_property

logger = logging.getLogger(__name__)


class SWAPIHandler:
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or settings.SWAPI_URL
        self.TEMP_FILE_PATH = settings.SWAPI_DATA_VAULT / "{filename}.jsonl"
        self.FINAL_FILE_PATH = settings.SWAPI_DATA_VAULT / "{filename}.csv"

    def pull_all(self, resource: str) -> Generator:
        url = urljoin(self.base_url, resource)
        page = 1
        while True:
            params = {"page": page}
            try:
                response = requests.get(url, params=params).json()
            except Exception as e:
                logger.error(e)
                raise

            data = response["results"]

            for item in data:
                yield item

            if not response["next"]:
                break

            page += 1

    @cached_property
    def planets_name_map(self) -> Mapping[str, str]:
        """Map planets' urls to their names. Cached to prevent API hammering."""
        return {p["url"]: p["name"] for p in self.pull_all("planets")}

    def _fetch_raw_people_data(self, raw_file_path: Union[Path, str]):
        """Fetches raw data and saves it to file."""
        with jsonlines.open(raw_file_path, "w", sort_keys=True) as raw_writer:
            raw_writer.write_all(self.pull_all("people"))

    def _transform_people_data(self, raw_file_path: Union[Path, str]) -> etl.Table:
        """Transforms raw data and returns etl Table"""

        cutout_fields = set(RawPerson.__annotations__.keys()) - set(Person.__annotations__.keys())

        raw_table = etl.fromjson(raw_file_path, lines=True, header=RawPerson.__annotations__.keys())

        return (
            raw_table.convert("homeworld", lambda url: self.planets_name_map[url])
            .addfield("date", lambda row: pendulum.parse(row["edited"]).date())
            .cutout(*cutout_fields)
        )

    # TODO: This should be called from celery
    def fetch_people(self, filename: Optional[str] = None) -> SwapiCollection:
        """Main workflow for fetching people. Returns created SwapiCollection."""
        # TODO: Use `tempfile` maybe?
        if filename is None:
            filename = uuid4().hex
        raw_file_path = str(self.TEMP_FILE_PATH).format(filename=filename)
        final_file_path = str(self.FINAL_FILE_PATH).format(filename=filename)

        self._fetch_raw_people_data(raw_file_path)
        transformed_data = self._transform_people_data(raw_file_path)
        transformed_data.tocsv(final_file_path)
        os.remove(raw_file_path)
        return SwapiCollection.objects.create(filename=final_file_path)
