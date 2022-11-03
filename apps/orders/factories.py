from factory import Faker, SubFactory, fuzzy
from factory.django import DjangoModelFactory, ImageField
from . import models
from apps.reviews.factories import ReviewFactory
from apps.users.factories import EmployeeFactory, ClientFactory
from apps.restaurants.factories import RestaurantFactory


class CategoryFactory(DjangoModelFactory):
    """Factory for Category instance."""

    name = Faker(
        "month_name",
    )

    class Meta:
        model = models.Category


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
    reviews = SubFactory(
        ReviewFactory,
    )

    class Meta:
        model = models.Dish


class OrderFactory(DjangoModelFactory):
    """Factory for Order instance."""

    status = fuzzy.FuzzyChoice(
        [item[0] for item in models.Order.Statuses.choices],
    )
    price = Faker(
        "pydecimal",
        left_digits=11,
        right_digits=2,
        min_value=50,
        max_value=5000,
    )
    comment = Faker(
        "text",
        max_nb_chars=30,
    )
    employee = SubFactory(
        EmployeeFactory
    )
    client = SubFactory(
        ClientFactory
    )
    place_number = Faker(
        "pyint",
        min_value=0,
        max_value=15,
    )
    dishes = SubFactory(
        DishFactory,
    )

    class Meta:
        model = models.Order


class DishImagesFactory(DjangoModelFactory):
    """Factory for DishImages instance."""

    image = ImageField(
        color="green",
    )
    dish = SubFactory(
        DishFactory,
    )

    class Meta:
        model = models.DishImages


class RestaurantAndOrderFactory(DjangoModelFactory):
    """Factory for RestaurantAndOrder instance."""

    arrival_time = Faker(
        "time",
    )
    order = SubFactory(
        OrderFactory,
    )
    restaurant = SubFactory(
        RestaurantFactory,
    )

    class Meta:
        model = models.RestaurantAndOrder
