import pytz
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from apps.orders.models import RestaurantAndOrder
from apps.restaurants.factories import RestaurantFactory

from .order_factory import OrderFactory


class RestaurantAndOrderFactory(DjangoModelFactory):
    """Factory for RestaurantAndOrder instance."""

    arrival_time = Faker(
        "date_time",
        tzinfo=pytz.UTC,
    )
    order = SubFactory(
        OrderFactory,
    )
    restaurant = SubFactory(
        RestaurantFactory,
    )

    class Meta:
        model = RestaurantAndOrder
