from apps.swexplorer.views import (
    CollectionDetailView,
    CollectionFetchView,
    CollectionInsightView,
    CollectionListView,
)
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("collections/", CollectionListView.as_view(), name="collection-list"),
    path("collections/fetch/", CollectionFetchView.as_view(), name="collection-fetch"),
    path("collections/<int:pk>/", CollectionDetailView.as_view(), name="collection-detail"),
    path(
        "collections/<int:pk>/insight/", CollectionInsightView.as_view(), name="collection-insight"
    ),
    path("", RedirectView.as_view(pattern_name="collection-list")),
]
