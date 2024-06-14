import random

from factory import (
    LazyAttribute,
    SubFactory,
    post_generation,
)
from factory.django import DjangoModelFactory

from apps.restaurants.models import Place, TagToPlace

from .restaurant import RestaurantFactory
from .tag_to_place import TagToPlaceFactory

TAGS_COUNT = 2


class PlaceFactory(DjangoModelFactory):
    """Factory for Place instance."""

    restaurant = SubFactory(
        RestaurantFactory,
    )
    place = LazyAttribute(
        lambda _: f"{'A' if random.randrange(1, 2) == 1 else 'B'}{random.randrange(1, 100)}",
    )

    @post_generation
    def tags(self, create, extracted, **kwargs):
        """Create tags for place."""
        if not create:
            return

        tags = []
        if extracted is not None:
            tags = extracted
        else:
            tags.append(TagToPlaceFactory(type=TagToPlace.Types.LOCATION))
            tags.append(TagToPlaceFactory(type=TagToPlace.Types.NUMBER_OF_SEATS))

        self.tags.add(*tags)

    class Meta:
        model = Place
        django_get_or_create = (
            "place",
            "restaurant",
        )
