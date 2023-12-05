from factory import (
    Faker,
    SubFactory,
    fuzzy,
)
from factory.django import DjangoModelFactory

from apps.orders.models import OrderAndDish
from apps.users.factories import EmployeeFactory

from . import DishFactory, OrderFactory


class OrderAndDishFactory(DjangoModelFactory):
    """Factory for OrderAndDish instance."""

    status = fuzzy.FuzzyChoice(
        [item[0] for item in OrderAndDish.Statuses.choices],
    )
    order = SubFactory(
        OrderFactory,
    )
    dish = SubFactory(
        DishFactory,
    )
    count = Faker(
        "pyint",
        min_value=1,
        max_value=10,
        step=1,
    )
    employee = SubFactory(
        EmployeeFactory,
    )

    class Meta:
        model = OrderAndDish
        django_get_or_create = (
            "dish",
            "order",
        )
