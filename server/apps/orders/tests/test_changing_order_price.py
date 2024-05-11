import pytest

from apps.orders.factories import (
    DishFactory,
    OrderAndDishFactory,
    OrderFactory,
)
from apps.orders.models import Order, OrderAndDish
from apps.users.factories import EmployeeFactory
from apps.users.models import Employee

pytestmark = pytest.mark.django_db

DISHES_NUMBER = 5


def test_change_order_price_by_changing_dish(
    cook,
) -> None:
    waiter = EmployeeFactory.create(
        restaurant=cook.restaurant,
        role=Employee.Roles.WAITER,
    )
    dishes = DishFactory.create_batch(size=DISHES_NUMBER)
    order = OrderFactory.create(
        status=Order.Statuses.WAITING_FOR_COOKING,
        employee=waiter,
    )

    price = 0
    order_and_dishes = []

    for dish in dishes:
        order_and_dishes.append(OrderAndDishFactory.create(
            order=order,
            dish=dish,
            status=OrderAndDish.Statuses.WAITING_FOR_COOKING,
            employee=None,
        ))
        price += dish.price

    assert order.price == price

    dish = order_and_dishes[-1]
    price -= dish.dish.price
    dish.status = OrderAndDish.Statuses.CANCELED
    dish.save()

    assert order.price == price
