from datetime import datetime

import pytz
from factory import LazyAttribute, SubFactory
from factory.django import DjangoModelFactory

from apps.orders.models import StopList
from apps.restaurants.factories import RestaurantFactory

from .dish import IngredientFactory


class StopListFactory(DjangoModelFactory):
    """Factory for StopList instance."""

    ingredient = SubFactory(
        IngredientFactory,
    )
    restaurant = SubFactory(
        RestaurantFactory,
    )
    created_at = LazyAttribute(
        lambda _: datetime.now(pytz.UTC)
    )

    class Meta:
        model = StopList
