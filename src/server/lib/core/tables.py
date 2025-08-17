from django_tables2 import tables
from .models import Trip


class TripTable(tables.Table):
    datetime = tables.Column(
        linkify=True,
        attrs={
            "td": {"class": "trip-datetime"},
            "th": {"class": "trip-datetime-header"},
        },
    )

    class Meta:
        model = Trip
        fields = ("datetime", "rider", "origin", "destination", "datetime")
        template_name = "core/daisyui_table.html"
        attrs = {
            "class": "table table-xs table-pin-rows table-pin-cols",
        }
