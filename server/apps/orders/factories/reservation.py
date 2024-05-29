from datetime import timedelta

from django.utils import timezone
from factory import (
    Faker,
    LazyAttribute,
    SubFactory,
    fuzzy,
)
from factory.django import DjangoModelFactory

from apps.orders.models import Reservation
from apps.restaurants.factories import (
    PlaceFactory,
    RestaurantFactory,
    TagToPlaceFactory,
)
from apps.users.factories import ClientFactory


class ReservationFactory(DjangoModelFactory):
    """Factory for Reservation instance."""

    status = fuzzy.FuzzyChoice(
        [item[0] for item in Reservation.Statuses.choices],
    )
    arrival_time = LazyAttribute(
        lambda _: timezone.now() + timedelta(days=2),
    )
    restaurant = SubFactory(
        RestaurantFactory,
    )
    client = SubFactory(
        ClientFactory,
    )
    place = SubFactory(
        PlaceFactory,
    )
    tag_to_place = SubFactory(
        TagToPlaceFactory,
    )
    count_guests = Faker(
        "pyint",
        min_value=1,
        max_value=20,
    )
    comment = Faker(
        "text",
        max_nb_chars=30,
    )

    class Meta:
        model = Reservation
