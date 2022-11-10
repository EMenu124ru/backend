from factory import Faker, SubFactory, post_generation
from factory.django import DjangoModelFactory

from apps.orders.models import Dish

from .category import CategoryFactory
from apps.reviews.factories import ReviewFactory

IMAGES_COUNT = REVIEWS_COUNT = 3


class DishFactory(DjangoModelFactory):
    """Factory for Dish instance."""

    category = SubFactory(
        CategoryFactory,
    )
    name = Faker(
        "language_name",
    )
    description = Faker(
        "text",
        max_nb_chars=15,
    )
    short_description = Faker(
        "text",
        max_nb_chars=5,
    )
    price = Faker(
        "pydecimal",
        left_digits=11,
        right_digits=2,
        min_value=50,
        max_value=1000,
    )
    compound = Faker(
        "text",
        max_nb_chars=20,
    )
    weight = Faker(
        "pydecimal",
        left_digits=11,
        right_digits=3,
        min_value=50,
        max_value=750,
    )

    @post_generation
    def reviews(self, create, extracted, **kwargs):
        if not create:
            return
        reviews = extracted if extracted is not None else (
            ReviewFactory(review=self) for _ in range(REVIEWS_COUNT)
        )
        self.reviews.add(*reviews)

    class Meta:
        model = Dish
