from factory import SubFactory
from factory.django import DjangoModelFactory

from apps.orders.models import OrderAndDishes

from . import DishFactory, OrderFactory


class OrderAndDishesFactory(DjangoModelFactory):
    """Factory for OrderAndDishes instance."""

    order = SubFactory(
        OrderFactory,
    )
    dish = SubFactory(
        DishFactory,
    )

    class Meta:
        model = OrderAndDishes
