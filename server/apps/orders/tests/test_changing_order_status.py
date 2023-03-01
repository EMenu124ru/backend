import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.orders.factories import DishFactory, OrderAndDishesFactory, OrderFactory
from apps.orders.models import Order, OrderAndDishes

pytestmark = pytest.mark.django_db

DISHES_NUMBER = 5


def test_change_order_status_by_changing_dish_status_success(
    cook,
    api_client,
) -> None:
    dishes = DishFactory.create_batch(size=DISHES_NUMBER)
    order = OrderFactory.create(
        price=sum([dish.price for dish in dishes]),
        status=Order.Statuses.WAITING_FOR_COOKING,
    )
    order_and_dishes = []
    for dish in dishes:
        order_and_dishes.append(
            OrderAndDishesFactory.create(
                order=order,
                dish=dish,
                status=OrderAndDishes.Statuses.WAITING_FOR_COOKING,
            ),
        )
    api_client.force_authenticate(user=cook.user)
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes[0].pk},
        ),
        data={
            "status": OrderAndDishes.Statuses.COOKING,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert OrderAndDishes.objects.filter(
        id=order_and_dishes[0].pk,
        status=OrderAndDishes.Statuses.COOKING,
        order__status=Order.Statuses.COOKING,
    ).exists()


def test_change_order_status_by_adding_new_dish(
    cook,
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
            OrderAndDishesFactory.create(
                order=order,
                dish=dish,
                status=OrderAndDishes.Statuses.DONE,
            ),
        )
    api_client.force_authenticate(user=cook.user)
    new_dish = DishFactory.create()
    response = api_client.post(
        reverse_lazy("api:orderAndDishes-list"),
        data={
            "order": order.pk,
            "dish": new_dish.pk,
            "status": OrderAndDishes.Statuses.COOKING,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert OrderAndDishes.objects.filter(
        dish=new_dish.pk,
        status=OrderAndDishes.Statuses.COOKING,
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
            OrderAndDishesFactory.create(
                order=order,
                dish=dish,
                status=OrderAndDishes.Statuses.WAITING_FOR_COOKING,
            ),
        )
    api_client.force_authenticate(user=client.user)
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes[0].pk},
        ),
        data={
            "status": OrderAndDishes.Statuses.COOKING,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert not OrderAndDishes.objects.filter(
        id=order_and_dishes[0].pk,
        status=OrderAndDishes.Statuses.COOKING,
        order__status=Order.Statuses.COOKING,
    ).exists()
