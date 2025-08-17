from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Account(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=20, blank=True, unique=True)
    avatar = models.URLField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Driver(models.Model):
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name="driver",
    )

    def __str__(self):
        return self.account.name


class Rider(models.Model):
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name="rider",
    )

    def __str__(self):
        return self.account.name


class TripStatus(models.TextChoices):
    scheduled = "scheduled", _("Scheduled")
    enroute = "enroute", _("En Route")
    arrived = "arrived", _("Arrived")
    in_progress = "in_progress", _("In Progress")
    completed = "completed", _("Completed")
    canceled = "canceled", _("Canceled")


class Trip(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="trips")
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE, related_name="trips")
    datetime = models.DateTimeField(null=True, blank=True)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=TripStatus.choices,
        default=TripStatus.scheduled,
    )

    def get_absolute_url(self):
        """This is used by the table to generate a link to the trip detail page."""
        return reverse("trip_detail", kwargs={"pk": self.pk})

    def clean(self):
        if self.driver.account.id == self.rider.account.id:
            raise ValidationError(
                "Driver cannot be assigned to a Trip when they are the Trip Rider."
            )

    def __str__(self):
        formatted_date = (
            self.datetime.strftime("%B %d, %Y") if self.datetime else "Unknown date"
        )
        return f"{self.rider.account.name} going to {self.destination} on {formatted_date} at {self.datetime.strftime('%I:%M %p') if self.datetime else 'Unknown time'}"
