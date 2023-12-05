from datetime import datetime, timedelta

import pytz
from factory import (
    Faker,
    LazyAttribute,
    SubFactory,
    fuzzy,
)
from factory.django import DjangoModelFactory

from apps.orders.models import Reservation
from apps.restaurants.factories import PlaceFactory, RestaurantFactory
from apps.users.factories import ClientFactory


class ReservationFactory(DjangoModelFactory):
    """Factory for Reservation instance."""

    status = fuzzy.FuzzyChoice(
        [item[0] for item in Reservation.Statuses.choices],
    )
    arrival_time = LazyAttribute(
        lambda _: datetime.now(pytz.UTC) + timedelta(days=2),
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
    comment = Faker(
        "text",
        max_nb_chars=30,
    )

    class Meta:
        model = Reservation
