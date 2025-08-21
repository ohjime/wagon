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


# ---------------------------------------------------------------------------
# Address generation
# ---------------------------------------------------------------------------
# We want realistic-looking (but fake) Canadian / Edmonton style addresses of
# the form: 8934 179A AVE NW Edmonton AB
# Pattern pieces:
#   <civic_number> <street_number>[<optional_letter>] <street_type> <direction> Edmonton AB
# Example output: 523 82 AVE NE Edmonton AB
#                 10432 179A ST NW Edmonton AB

STREET_TYPES = ["AVE", "ST", "RD", "DR", "CT", "PL", "BLVD", "WAY", "TRAIL"]
CARDINALS = ["NW", "NE", "SW", "SE"]
LETTER_SUFFIXES = ["", "A", "B", "C"]  # appended to street number occasionally


def generate_address() -> str:
    civic_number = random.randint(1, 99999)  # Edmonton civic numbers can be large
    street_number = random.randint(1, 300)
    letter = random.choice(LETTER_SUFFIXES)
    # Lower probability for a letter suffix; keep only ~20% of the time
    if letter and random.random() > 0.2:
        letter = ""
    street_type = random.choice(STREET_TYPES)
    direction = random.choice(CARDINALS)
    return (
        f"{civic_number} {street_number}{letter} {street_type} {direction} Edmonton AB"
    )


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
    origin = LazyFunction(generate_address)
    status = models.TripStatus.scheduled

    @factory.lazy_attribute  # type: ignore
    def destination(self):  # type: ignore
        # Ensure destination differs from origin; regenerate until different (cap tries)
        for _ in range(5):
            addr = generate_address()
            if addr != self.origin:
                return addr
        return generate_address()

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
                    origin=generate_address(),
                    destination=generate_address(),
                    status=models.TripStatus.scheduled,
                )
            )
        created = models.Trip.objects.bulk_create(trips)
        return created


# Convenience: create N trips with separate drivers/riders
def create_sample_trips(count=25):
    return TripFactory.bulk(count)
