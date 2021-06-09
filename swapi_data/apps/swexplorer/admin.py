from apps.swexplorer.models import SwapiCollection
from django.contrib import admin


@admin.register(SwapiCollection)
class SwapiCollectionAdmin(admin.ModelAdmin):
    list_display_links = list_display = (
        "date",
        "filename",
    )
    date_hierarchy = "date"
