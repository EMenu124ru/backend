import random

from factory import LazyAttribute, SubFactory, post_generation
from factory.django import DjangoModelFactory

from apps.restaurants.models import Place

from .restaurant import RestaurantFactory
from .tag_to_place import TagToPlaceFactory


TAGS_COUNT = 10


class PlaceFactory(DjangoModelFactory):
    """Factory for Place instance."""

    restaurant = SubFactory(
        RestaurantFactory,
    )
    place = LazyAttribute(
        lambda _: f"A{random.randrange(1, 30)}",
    )

    @post_generation
    def tags(self, create, extracted, **kwargs):
        """Create tags for place."""
        if not create:
            return
        tags = extracted if extracted is not None else (
            TagToPlaceFactory() for _ in range(TAGS_COUNT)
        )
        self.tags.add(*tags)

    class Meta:
        model = Place
        django_get_or_create = (
            "place",
        )
