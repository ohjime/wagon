from django.urls import path
from core.views import trips_index, riders_index, drivers_index, index, TripDetailView


urlpatterns = [
    path("", index, name="core_index"),
    path("trips/", trips_index, name="trips_index"),
    path("riders/", riders_index, name="riders_index"),
    path("drivers/", drivers_index, name="drivers_index"),
    path("<str:pk>/", TripDetailView.as_view(), name="trip_detail"),
]
