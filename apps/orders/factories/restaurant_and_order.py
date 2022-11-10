from datetime import datetime, timedelta

from factory import LazyAttribute, SubFactory
from factory.django import DjangoModelFactory

from apps.orders.models import RestaurantAndOrder
from apps.restaurants.factories import RestaurantFactory

from .order import OrderFactory


class RestaurantAndOrderFactory(DjangoModelFactory):
    """Factory for RestaurantAndOrder instance."""

    arrival_time = LazyAttribute(
        lambda _: datetime.today() + timedelta(days=2),
    )
    order = SubFactory(
        OrderFactory,
    )
    restaurant = SubFactory(
        RestaurantFactory,
    )

    class Meta:
        model = RestaurantAndOrder
