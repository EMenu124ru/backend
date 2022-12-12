from factory import SubFactory, fuzzy
from factory.django import DjangoModelFactory

from apps.restaurants.factories import RestaurantFactory
from apps.users.models import Employee

from .user import UserFactory


class EmployeeFactory(DjangoModelFactory):
    """Factory for Employee instance."""

    user = SubFactory(
        UserFactory,
    )
    role = fuzzy.FuzzyChoice(
        [item[0] for item in Employee.Roles.choices],
    )
    restaurant = SubFactory(
        RestaurantFactory,
    )

    class Meta:
        model = Employee
