from factory import SubFactory
from factory.django import DjangoModelFactory

from apps.orders.models import StopList
from apps.restaurants.factories import RestaurantFactory

from .dish import DishFactory


class StopListFactory(DjangoModelFactory):
    """Factory for StopList instance."""

    dish = SubFactory(
        DishFactory,
    )
    restaurant = SubFactory(
        RestaurantFactory,
    )

    class Meta:
        model = StopList
