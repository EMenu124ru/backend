from factory import Faker, SubFactory, fuzzy
from factory.django import DjangoModelFactory, ImageField
from apps.users.factories import ClientFactory
from . import models


class ReviewFactory(DjangoModelFactory):
    """Factory for Review instance."""

    review = Faker(
        "text",
        max_nb_chars=25,
    )
    mark = Faker(
        "pyint",
        min_value=1,
        max_value=5,
        step=1,
    )
    client = SubFactory(
        ClientFactory,
    )
    email = Faker(
        "email",
    )
    password = Faker(
        "password",
    )

    class Meta:
        model = models.Review



class ReviewImagesFactpry(DjangoModelFactory):
    """Factory for ReviewImages instance."""

    image = ImageField(
        color="green",
    )
    review = SubFactory(
        ReviewFactory,
    )

    class Meta:
        model = models.ReviewImages
