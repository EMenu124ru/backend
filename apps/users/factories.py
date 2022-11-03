from factory import Faker, SubFactory, fuzzy
from factory.django import DjangoModelFactory
from . import models
from apps.restaurants.factories import RestaurantFactory


class UserFactory(DjangoModelFactory):
    """Factory for User instance."""

    first_name = Faker(
        "first_name",
    )
    last_name = Faker(
        "last_name",
    )
    email = Faker(
        "email",
    )
    password = Faker(
        "password",
    )

    class Meta:
        model = models.User


class ClientFactory(DjangoModelFactory):
    """Factory for Client instance."""

    user = SubFactory(
        UserFactory,
    )
    bonuses = Faker(
        "pyint",
        min_value=0,
        max_value=250,
        step=1,
    )
    phone_number = Faker(
        "phone_number",
    )

    class Meta:
        model = models.Client


class EmployeeFactory(DjangoModelFactory):
    """Factory for Employee instance."""

    user = SubFactory(
        UserFactory,
    )
    role = fuzzy.FuzzyChoice(
        [item[0] for item in models.Employee.Roles.choices],
    )
    restaraunt = SubFactory(
        RestaurantFactory,
    )

    class Meta:
        model = models.Employee
