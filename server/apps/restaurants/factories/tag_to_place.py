from factory import Faker
from factory.django import DjangoModelFactory

from apps.restaurants.models import TagToPlace


class TagToPlaceFactory(DjangoModelFactory):
    """Factory for TagToPlace instance."""

    name = Faker(
        "first_name",
    )

    class Meta:
        model = TagToPlace
        django_get_or_create = (
            "name",
        )
