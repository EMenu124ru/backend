from factory import (
    Faker,
    SubFactory,
    fuzzy,
)
from factory.django import DjangoModelFactory

from apps.orders.models import Order
from apps.users.factories import ClientFactory, EmployeeFactory

from .reservation import ReservationFactory


class OrderFactory(DjangoModelFactory):
    """Factory for Order instance."""

    status = fuzzy.FuzzyChoice(
        [item[0] for item in Order.Statuses.choices],
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
        EmployeeFactory,
    )
    client = SubFactory(
        ClientFactory,
    )
    reservation = SubFactory(
        ReservationFactory,
    )

    class Meta:
        model = Order
