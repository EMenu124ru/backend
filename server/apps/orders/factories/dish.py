from factory import Faker, SubFactory
from factory.django import DjangoModelFactory, ImageField

from apps.orders.models import Ingredient, Dish, DishImage

from .category import CategoryFactory


class IngredientFactory(DjangoModelFactory):
    """Factory for Ingredient instance."""

    name = Faker(
        "language_name",
    )

    class Meta:
        model = Ingredient


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

    class Meta:
        model = Dish


class DishImageFactory(DjangoModelFactory):
    """Factory for DishImage instance."""

    image = ImageField(
        color="green",
    )
    dish = SubFactory(
        DishFactory,
    )

    class Meta:
        model = DishImage
