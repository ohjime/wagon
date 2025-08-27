from django_tables2 import RequestConfig
from .models import Trip
from .tables import TripTable
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.db.models import Q


def trips_index(request):
    table = TripTable(Trip.objects.all())
    RequestConfig(request, paginate={"per_page": 80}).configure(table)  # type: ignore
    if request.htmx:
        template_name = "core/trips/partials/list.html"
    else:
        template_name = "core/trips/trips.html"
    return render(request, template_name, {"table": table})


# Search/filtering of trips table
def table_htmx(request):
    import time

    time.sleep(1)
    query = request.GET.get("search", "").strip()
    qs = Trip.objects.all()
    if query:
        qs = qs.filter(
            Q(id__icontains=query)
            | Q(rider__account__name__icontains=query)
            | Q(driver__account__name__icontains=query)
            | Q(origin__icontains=query)
            | Q(destination__icontains=query)
        )
    table = TripTable(qs)
    RequestConfig(request, paginate={"per_page": 80}).configure(table)  # type: ignore
    return render(request, "core/trips/partials/list.html", {"table": table})


def riders_index(request):
    if request.htmx:
        template_name = "core/riders/partials/list.html"
    else:
        template_name = "core/riders/riders.html"
    return render(request, template_name)


def drivers_index(request):
    if request.htmx:
        template_name = "core/drivers/partials/list.html"
    else:
        template_name = "core/drivers/drivers.html"
    return render(request, template_name)


def index(request):
    template_name = "core/index.html"
    return render(request, template_name)


class TripDetailView(DetailView):
    model = Trip
    template_name = "core/trip_detail.html"
