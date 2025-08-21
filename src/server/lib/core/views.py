from django_tables2 import RequestConfig
from .models import Trip
from .tables import TripTable
from django.shortcuts import render
from django.views.generic.detail import DetailView


def trips_index(request):
    table = TripTable(Trip.objects.all())
    RequestConfig(request, paginate={"per_page": 80}).configure(table)  # type: ignore
    if request.htmx:
        template_name = "core/trips/partials/list.html"
    else:
        template_name = "core/trips/trips.html"
    return render(request, template_name, {"table": table})


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
