from factory import (
    Faker,
    LazyAttribute,
    SubFactory,
    post_generation,
)
from factory.django import DjangoModelFactory, ImageField

from apps.core.factories import ObjectFileFactory
from apps.orders.models import (
    Dish,
    DishImage,
    Ingredient,
)

from .category import CategoryFactory

INGREDIENTS_COUNT = 5
DISH_IMAGES_COUNT = 3


class IngredientFactory(DjangoModelFactory):
    """Factory for Ingredient instance."""

    name = Faker(
        "language_name",
    )

    class Meta:
        django_get_or_create = (
            "name",
        )
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

    @post_generation
    def ingredients(self, create, extracted, **kwargs):
        """Create ingredients for dish."""
        if not create:
            return
        ingredients = extracted if extracted is not None else (
            IngredientFactory() for _ in range(INGREDIENTS_COUNT)
        )
        self.ingredients.add(*ingredients)

    @post_generation
    def images(self, create, extracted, **kwargs):
        """Create images for dish."""
        if not create:
            return
        images = extracted if extracted is not None else (
            DishImageFactory(dish=self) for _ in range(DISH_IMAGES_COUNT)
        )
        self.images.add(*images)

    class Meta:
        model = Dish


class DishImageFactory(DjangoModelFactory):
    """Factory for DishImage instance."""

    image = LazyAttribute(
        lambda _: ObjectFileFactory.create(file=ImageField()),
    )
    dish = SubFactory(
        DishFactory,
    )

    class Meta:
        model = DishImage
