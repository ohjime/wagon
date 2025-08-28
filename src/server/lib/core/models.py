from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from sqids import Sqids
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.urls import reverse
from app.db import BaseModel


class User(AbstractUser):
    pass


class Account(models.Model):
    uid = models.CharField(max_length=128, unique=True, db_index=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255, blank=True, unique=True)
    avatar = models.URLField(max_length=255, blank=True)

    def __str__(self):
        return self.email


class Driver(models.Model):
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name="driver",
    )

    def __str__(self):
        return self.account.first_name + " " + self.account.last_name


class Rider(models.Model):
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name="rider",
    )

    def __str__(self):
        return self.account.first_name + " " + self.account.last_name


class TripStatus(models.TextChoices):
    scheduled = "scheduled", _("Scheduled")
    assigned = "assigned", _("Assigned")
    enroute = "enroute", _("En Route")
    arrived = "arrived", _("Arrived")
    in_progress = "in_progress", _("In Progress")
    completed = "completed", _("Completed")
    canceled = "canceled", _("Canceled")


DEFAULT_LOCATION_POINT = Point(-104.9903, 39.7392)


class Place(BaseModel):
    id = models.CharField(primary_key=True, max_length=255, unique=True, db_index=True)
    address = models.CharField(max_length=255)
    coordinate = models.PointField(blank=True, null=True)

    def __str__(self) -> str:
        return self.address


class Trip(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="trips")
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE, related_name="trips")
    date = models.DateTimeField(null=True, blank=True)
    origin = models.ForeignKey(
        Place, on_delete=models.PROTECT, related_name="trips_origin"
    )
    destination = models.ForeignKey(
        Place, on_delete=models.PROTECT, related_name="trips_destination"
    )
    hashid = models.CharField(max_length=32, unique=True, db_index=True)
    status = models.CharField(
        max_length=20,
        choices=TripStatus.choices,
        default=TripStatus.scheduled,
    )

    customer_notes = models.TextField(blank=True, default="")
    driver_notes = models.TextField(blank=True, default="")
    dispatcher_notes = models.TextField(blank=True, default="")

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.hashid:
            sqids = Sqids(
                min_length=10, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
            )
            encoded = sqids.encode([self.pk, self.rider_id, self.driver_id])  # type: ignore
            Trip.objects.filter(pk=self.pk).update(hashid=encoded)
            self.hashid = encoded

    def get_absolute_url(self):
        """This is used by the table to generate a link to the trip detail page."""
        return reverse("trip_detail", kwargs={"pk": self.pk})

    def clean(self):
        if self.driver.account.uid == self.rider.account.uid:
            raise ValidationError(
                "Driver cannot be assigned to a Trip when they are the Trip Rider."
            )

    def __str__(self):
        formatted_date = (
            self.date.strftime("%B %d, %Y") if self.date else "Unknown date"
        )
        return f"Trip for {self.rider} going from {self.origin} to {self.destination} on {formatted_date} at {self.date.strftime('%I:%M %p') if self.date else 'Unknown time'}"
