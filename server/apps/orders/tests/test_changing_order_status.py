import pytest
from django.urls import reverse_lazy
from rest_framework import status

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


def test_change_order_status_by_changing_dish_status_success(
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
    order_and_dishes = []
    for dish in dishes:
        order_and_dishes.append(
            OrderAndDishFactory.create(
                order=order,
                dish=dish,
                status=OrderAndDish.Statuses.WAITING_FOR_COOKING,
                employee=None,
            ),
        )

    assert order.status == Order.Statuses.WAITING_FOR_COOKING

    for dish in order_and_dishes:
        dish.employee = cook
        dish.save()
        assert dish.status == OrderAndDish.Statuses.COOKING

    assert order.status == Order.Statuses.COOKING

    for dish in order_and_dishes:
        dish.status = OrderAndDish.Statuses.DONE
        dish.save()
        assert order.status == Order.Statuses.WAITING_FOR_DELIVERY

    for dish in order_and_dishes:
        dish.status = OrderAndDish.Statuses.DELIVERED
        dish.save()
    assert order.status == Order.Statuses.DELIVERED

    for dish in order_and_dishes:
        dish.employee = cook
        dish.save()
        assert dish.status == OrderAndDish.Statuses.DELIVERED


def test_change_order_status_by_adding_new_dish(
    waiter,
) -> None:
    cook = EmployeeFactory.create(
        restaurant=waiter.restaurant,
        role=Employee.Roles.COOK,
    )
    dishes = DishFactory.create_batch(size=DISHES_NUMBER)
    order = OrderFactory.create(
        status=Order.Statuses.WAITING_FOR_DELIVERY,
    )
    order_and_dishes = []
    for dish in dishes:
        order_and_dishes.append(
            OrderAndDishFactory.create(
                order=order,
                dish=dish,
                status=OrderAndDish.Statuses.DONE,
            ),
        )
    new_dish = DishFactory.create()
    order_and_dish = OrderAndDishFactory.create(
        order=order,
        dish=new_dish,
        status=OrderAndDish.Statuses.WAITING_FOR_COOKING,
        employee=None,
    )
    assert order.status == Order.Statuses.WAITING_FOR_COOKING

    order_and_dish.employee = cook
    order_and_dish.save()
    assert order_and_dish.status == OrderAndDish.Statuses.COOKING
    assert order.status == Order.Statuses.WAITING_FOR_DELIVERY

    for dish in order_and_dishes:
        dish.status = OrderAndDish.Statuses.DELIVERED
        dish.save()
    assert order.status == Order.Statuses.COOKING

    order_and_dish.status = OrderAndDish.Statuses.DONE
    order_and_dish.save()
    assert order.status == Order.Statuses.WAITING_FOR_DELIVERY

    order_and_dish.status = OrderAndDish.Statuses.DELIVERED
    order_and_dish.save()
    assert order.status == Order.Statuses.DELIVERED


def test_change_order_status_by_cancel_dish() -> None:
    dishes = DishFactory.create_batch(size=DISHES_NUMBER)
    order = OrderFactory.create(
        status=Order.Statuses.WAITING_FOR_DELIVERY,
    )
    order_and_dishes = []
    for dish in dishes:
        order_and_dishes.append(
            OrderAndDishFactory.create(
                order=order,
                dish=dish,
                status=OrderAndDish.Statuses.DONE,
            ),
        )
    new_dish = DishFactory.create()
    order_and_dish = OrderAndDishFactory.create(
        order=order,
        dish=new_dish,
        status=OrderAndDish.Statuses.WAITING_FOR_COOKING,
        employee=None,
    )
    assert order.status == Order.Statuses.WAITING_FOR_COOKING

    order_and_dish_id = order_and_dish.id
    order_and_dish.status = OrderAndDish.Statuses.CANCELED
    order_and_dish.save()

    assert not OrderAndDish.objects.filter(pk=order_and_dish_id).exists()
    assert order.status == Order.Statuses.WAITING_FOR_DELIVERY


def test_change_order_status_by_changing_dish_status_failed(
    client,
    api_client
) -> None:
    dishes = DishFactory.create_batch(size=DISHES_NUMBER)
    order = OrderFactory.create(
        status=Order.Statuses.WAITING_FOR_COOKING,
    )
    order_and_dishes = []
    for dish in dishes:
        order_and_dishes.append(
            OrderAndDishFactory.create(
                order=order,
                dish=dish,
                status=OrderAndDish.Statuses.WAITING_FOR_COOKING,
            ),
        )
    api_client.force_authenticate(user=client.user)
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes[0].pk},
        ),
        data={
            "status": OrderAndDish.Statuses.COOKING,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert not OrderAndDish.objects.filter(
        id=order_and_dishes[0].pk,
        status=OrderAndDish.Statuses.COOKING,
        order__status=Order.Statuses.COOKING,
    ).exists()
