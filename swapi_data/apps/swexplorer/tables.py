import django_tables2 as tables
from django_tables2.utils import A

from .models import SwapiCollection


class SwapiCollectionsTable(tables.Table):
    date = tables.LinkColumn("collection-detail", args=[A("pk")])

    class Meta:
        model = SwapiCollection
        template_name = "django_tables2/bootstrap.html"
        fields = ("date",)
