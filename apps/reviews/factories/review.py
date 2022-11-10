from factory import Faker, SubFactory, post_generation
from factory.django import DjangoModelFactory

from apps.reviews.models import Review
from apps.users.factories import ClientFactory

IMAGES_COUNT = 3


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

    class Meta:
        model = Review
