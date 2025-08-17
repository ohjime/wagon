import random
import uuid
import factory
from datetime import datetime, timedelta

from factory.declarations import LazyFunction, SubFactory
from factory import post_generation  # type: ignore
from factory.faker import Faker
from core import models


class AccountFactory(factory.django.DjangoModelFactory):
    """Base account used by Driver/Rider factories."""

    class Meta:  # type: ignore
        model = models.Account

    id = Faker("uuid4")
    name = Faker("name")
    email = Faker("email")
    phone = Faker("phone_number")

    @factory.lazy_attribute  # type: ignore
    def avatar(self):
        return f"https://i.pravatar.cc/150?u={self.id}"


class DriverFactory(factory.django.DjangoModelFactory):
    class Meta:  # type: ignore
        model = models.Driver

    account = SubFactory(AccountFactory)  # type: ignore[misc]


class RiderFactory(factory.django.DjangoModelFactory):
    class Meta:  # type: ignore
        model = models.Rider

    account = SubFactory(AccountFactory)  # type: ignore[misc]


ORIGINS = [
    "Central Station",
    "Airport Terminal",
    "Harbor Dock",
    "University Campus",
    "Tech Park",
]
DESTINATIONS = [
    "City Mall",
    "Hotel Plaza",
    "Convention Center",
    "Museum District",
    "Old Town",
]


def _random_time_window():
    """Return a datetime within +/- 3 days from now."""
    now = datetime.utcnow()
    delta = timedelta(hours=random.randint(-72, 72), minutes=random.randint(0, 59))
    return now + delta


class TripFactory(factory.django.DjangoModelFactory):
    class Meta:  # type: ignore
        model = models.Trip

    id = Faker("uuid4")
    driver = SubFactory(DriverFactory)  # type: ignore[misc]
    rider = SubFactory(RiderFactory)  # type: ignore[misc]
    datetime = LazyFunction(_random_time_window)
    origin = LazyFunction(lambda: random.choice(ORIGINS))
    status = models.TripStatus.scheduled

    @factory.lazy_attribute  # type: ignore
    def destination(self):  # type: ignore
        # Ensure origin != destination sometimes
        dest_choices = [d for d in DESTINATIONS if d != self.origin]
        return (
            random.choice(dest_choices) if dest_choices else random.choice(DESTINATIONS)
        )

    @post_generation  # type: ignore
    def ensure_distinct_accounts(self, create, extracted, **kwargs):  # type: ignore
        if not create:
            return
        # If accidently same Account (should almost never happen because of UUID faker) regenerate rider.
        if self.driver.account_id == self.rider.account_id:  # type: ignore[attr-defined]
            self.rider = RiderFactory()
            self.save(update_fields=["rider_id"])  # type: ignore[arg-type]

    @classmethod
    def bulk(cls, count: int, **overrides):
        """Efficiently create many trips.

        Uses Django bulk_create for speed. Note: post_generation hooks
        don't run for bulk_create, so we manually enforce account distinctness.
        """
        trips = []
        for _ in range(count):
            driver = overrides.get("driver") or DriverFactory()
            rider = overrides.get("rider") or RiderFactory()
            # Ensure distinct accounts
            if driver.account_id == rider.account_id:
                rider = RiderFactory()
            trips.append(
                models.Trip(
                    id=str(uuid.uuid4()),
                    driver=driver,
                    rider=rider,
                    datetime=_random_time_window(),
                    origin=random.choice(ORIGINS),
                    destination=random.choice(DESTINATIONS),
                    status=models.TripStatus.scheduled,
                )
            )
        created = models.Trip.objects.bulk_create(trips)
        return created


# Convenience: create N trips with separate drivers/riders
def create_sample_trips(count=25):
    return TripFactory.bulk(count)
