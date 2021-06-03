from urllib.parse import urlencode

import django_tables2 as tables
import petl
from django.views.generic import DetailView, RedirectView

from .handlers import SWAPIHandler
from .models import SwapiCollection
from .tables import SwapiCollectionsTable


class CollectionListView(tables.SingleTableView):
    model = SwapiCollection
    table_class = SwapiCollectionsTable
    paginator_class = tables.LazyPaginator


class CollectionDetailView(DetailView):
    model = SwapiCollection

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        amount = int(self.request.GET.get("load", 10))
        context["next_amount"] = amount + 10
        context["data"] = self.object.get_data().islice(amount)
        return context


class CollectionInsightView(DetailView):
    model = SwapiCollection
    template_name = "swexplorer/swapicollection_insight.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chosen = self.request.GET.getlist("chosen", None)
        key = chosen[0] if len(chosen) == 1 else chosen
        context["chosen"] = chosen
        context["fields"] = self._resolve_fields(chosen)
        context["data"] = self.object.get_data().cut(*chosen).aggregate(key=key, aggregation=len)
        return context

    def _resolve_fields(self, chosen):
        chosen = set(chosen)
        fields = petl.header(self.object.get_data())
        prepared_fields = []
        for field_name in fields:
            if field_name in chosen:
                url = urlencode({"chosen": chosen ^ {field_name}}, doseq=True)
            else:
                url = urlencode({"chosen": chosen | {field_name}}, doseq=True)
            prepared_fields.append(
                {
                    "name": field_name,
                    "url": f"?{url}" if url else "",
                }
            )
        return prepared_fields


class CollectionFetchView(RedirectView):
    permanent = False
    pattern_name = "collection-list"

    def get_redirect_url(self, *args, **kwargs):
        handler = SWAPIHandler()
        handler.fetch_people()
        # TODO: handle `show_detail=1` GET param to be redirected to see new collection after creation
        return super().get_redirect_url(*args, **kwargs)
