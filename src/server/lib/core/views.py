from django_tables2 import RequestConfig
from .models import Trip, Place
from .tables import TripTable
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.http import HttpRequest
from django.http import HttpResponseRedirect


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

    def get_template_names(self):
        request: HttpRequest = self.request  # type: ignore
        if getattr(request, "htmx", False):
            return ["core/trips/partials/details.html"]
        return [self.template_name]

    def post(self, request: HttpRequest, *args, **kwargs):  # type: ignore
        self.object = self.get_object()
        origin_address = request.POST.get("origin_address", "").strip()
        destination_address = request.POST.get("destination_address", "").strip()
        origin_id = request.POST.get("origin_id", "").strip()
        destination_id = request.POST.get("destination_id", "").strip()

        # Upsert origin Place
        if origin_address and origin_id:
            origin_place, _ = Place.objects.update_or_create(
                place_id=origin_id,
                defaults={"address": origin_address},
            )
            self.object.origin = origin_place  # type: ignore

        # Upsert destination Place
        if destination_address and destination_id:
            destination_place, _ = Place.objects.update_or_create(
                place_id=destination_id,
                defaults={"address": destination_address},
            )
            self.object.destination = destination_place  # type: ignore

        # Optionally parse lat/lng to set coordinate if posted (not shown here)

        self.object.full_clean(exclude=["hashid"])  # validate model constraints
        self.object.save()

        if getattr(request, "htmx", False):
            context = self.get_context_data(object=self.object)
            return render(request, "core/trips/partials/details.html", context)
        return HttpResponseRedirect(self.object.get_absolute_url())
