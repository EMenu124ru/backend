import random

from factory import LazyAttribute, SubFactory
from factory.django import DjangoModelFactory

from apps.restaurants.models import Place

from .restaurant import RestaurantFactory


class PlaceFactory(DjangoModelFactory):
    """Factory for Place instance."""

    restaurant = SubFactory(
        RestaurantFactory,
    )
    place = LazyAttribute(
        lambda _: f"A{random.randrange(1, 30)}",
    )

    class Meta:
        model = Place
        django_get_or_create = (
            "place",
        )
