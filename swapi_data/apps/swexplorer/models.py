import petl
from django.conf import settings
from django.db import models


class SwapiCollection(models.Model):
    filename = models.FilePathField(path=settings.SWAPI_DATA_VAULT)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"<Collection dated {self.date}>"

    def get_data(self) -> petl.Table:
        return petl.fromcsv(self.filename)
