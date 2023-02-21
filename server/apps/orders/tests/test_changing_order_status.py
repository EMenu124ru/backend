import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.orders.factories import DishFactory, OrderFactory, OrderAndDishesFactory
from apps.orders.models import Order, OrderAndDishes

pytestmark = pytest.mark.django_db

DISHES_NUMBER = 5

def test_change_order_status_by_changing_dish_status(
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
    ).exists()
    new_order = Order.objects.get(id=order.pk)
    print(new_order.status)
    assert Order.objects.filter(
        id=order.pk,
        status=Order.Statuses.COOKING,
    ).exists()


# def changing_order_status_by_adding_new_dish(
#     cook,
#     api_client,
# ):
#     dishes = DishFactory.create_batch(size=DISHES_NUMBER)
#     order = OrderFactory.create(
#         price=sum([dish.price for dish in dishes]),
#         status=Order.Statuses.WAITING_FOR_COOKING,
#     )
#     order_and_dishes = []
#     for dish in dishes:
#         order_and_dishes.append(
#             OrderAndDishesFactory.create(
#                 order=order,
#                 dish=dish,
#                 status=OrderAndDishes.Statuses.WAITING_FOR_COOKING,
#             ),
#         )
#     api_client.force_authenticate(user=cook.user)
#     new
