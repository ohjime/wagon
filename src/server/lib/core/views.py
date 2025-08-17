from django_tables2 import RequestConfig
from .models import Trip
from .tables import TripTable
from django.shortcuts import render
from django.views.generic.detail import DetailView


def all_trips(request):
    template_name = "core/all_trips.html"
    table = TripTable(Trip.objects.all())
    RequestConfig(request, paginate={"per_page": 5}).configure(table)  # type: ignore
    return render(request, template_name, {"table": table})


class TripDetailView(DetailView):
    model = Trip
    template_name = "core/trip_detail.html"
