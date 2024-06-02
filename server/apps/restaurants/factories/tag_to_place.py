from factory import Faker, fuzzy
from factory.django import DjangoModelFactory

from apps.restaurants.models import TagToPlace


class TagToPlaceFactory(DjangoModelFactory):
    """Factory for TagToPlace instance."""

    name = Faker(
        "first_name",
    )
    type = fuzzy.FuzzyChoice(
        [item[0] for item in TagToPlace.Types.choices],
    )

    class Meta:
        model = TagToPlace
        django_get_or_create = (
            "name",
        )
