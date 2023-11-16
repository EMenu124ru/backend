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
    api_client,
) -> None:
    waiter = EmployeeFactory.create(
        restaurant=cook.restaurant,
        role=Employee.Roles.WAITER,
    )
    dishes = DishFactory.create_batch(size=DISHES_NUMBER)
    order = OrderFactory.create(
        price=sum([dish.price for dish in dishes]),
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
                employee=cook,
            ),
        )
    api_client.force_authenticate(user=cook.user)
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes[0].pk},
        ),
        data={
            "status": OrderAndDish.Statuses.COOKING,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert OrderAndDish.objects.filter(
        id=order_and_dishes[0].pk,
        status=OrderAndDish.Statuses.COOKING,
        order__status=Order.Statuses.COOKING,
    ).exists()


def test_change_order_status_by_adding_new_dish(
    waiter,
    api_client,
) -> None:
    dishes = DishFactory.create_batch(size=DISHES_NUMBER)
    order = OrderFactory.create(
        price=sum([dish.price for dish in dishes]),
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
    api_client.force_authenticate(user=waiter.user)
    new_dish = DishFactory.create()
    response = api_client.post(
        reverse_lazy("api:orderAndDishes-list"),
        data={
            "order": order.pk,
            "dish": new_dish.pk,
            "status": OrderAndDish.Statuses.COOKING,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert OrderAndDish.objects.filter(
        dish=new_dish.pk,
        status=OrderAndDish.Statuses.COOKING,
        order__status=Order.Statuses.COOKING,
    ).exists()


def test_change_order_status_by_changing_dish_status_failed(
    client,
    api_client
) -> None:
    dishes = DishFactory.create_batch(size=DISHES_NUMBER)
    order = OrderFactory.create(
        price=sum([dish.price for dish in dishes]),
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
