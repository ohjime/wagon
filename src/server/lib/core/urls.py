from django.urls import path
from core.views import all_trips, TripDetailView

urlpatterns = [
    path("", all_trips, name="all_trips"),
    path("", all_trips, name="all_drivers"),
    path("", all_trips, name="all_riders"),
    path("", all_trips, name="settings"),
    path("<str:pk>/", TripDetailView.as_view(), name="trip_detail"),
]
