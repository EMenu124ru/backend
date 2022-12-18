import pytest
from django.urls import reverse_lazy
from rest_framework import status
from apps.orders.factories import RestaurantAndOrderFactory, OrderFactory, DishFactory
from apps.users.factories import EmployeeFactory, ClientFactory
from apps.restaurants.factories import RestaurantFactory
from apps.orders.models import RestaurantAndOrder

pytestmark = pytest.mark.django_db


def test_create_rest_and_order_by_waiter(
    waiter,
    api_client,
) -> None:
    order = OrderFactory.build()
    restaurant = RestaurantFactory.build()
    rest_and_order = RestaurantAndOrderFactory.build(
        order=order,
        restaurant=restaurant,
    )
    api_client.force_authenticate(user=waiter.user)
    response = api_client.post(
        reverse_lazy("api:restaurantAndOrders-list"),
        data={
            "order": rest_and_order.order.pk,
            "restaurant": rest_and_order.restaurant.pk,
            "arrival_time": rest_and_order.arrival_time,
            "place_number": rest_and_order.place_number,
        },
        format='json',
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert RestaurantAndOrder.objects.filter(
        order=order.pk,
        restaurant=restaurant.pk,
        arrival_time=rest_and_order.arrival_time,
        place_number=rest_and_order.place_number,
    ).exists()


def test_read_rest_and_order_by_waiter(
    waiter,
    api_client,
) -> None:
    order = OrderFactory.create()
    restaurant = RestaurantFactory.create()
    rest_and_order = RestaurantAndOrderFactory.create(
        order=order,
        restaurant=restaurant,
    )
    api_client.force_authenticate(user=waiter.user)
    response = api_client.get(
        reverse_lazy(
            "api:restaurantAndOrders-detail",
            kwargs={"pk": rest_and_order.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_update_rest_and_order_by_waiter(
    waiter,
    api_client,
) -> None:
    order = OrderFactory.create()
    restaurant = RestaurantFactory.create()
    rest_and_order = RestaurantAndOrderFactory.create(
        order=order,
        restaurant=restaurant,
    )
    new_order = OrderFactory.create()
    api_client.force_authenticate(user=waiter.user)
    response = api_client.patch(
        reverse_lazy(
            "api:restaurantAndOrders-detail",
            kwargs={"pk": rest_and_order.pk},
        ),
        data={
            "order": new_order,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    # тут такого объекта не находит
    assert RestaurantAndOrder.objects.filter(
        order=new_order,
        restaurant=restaurant,
        arrival_time=rest_and_order.arrival_time,
        place_number=rest_and_order.place_number,
    ).exists()


def test_remove_rest_and_order_by_waiter(
    waiter,
    api_client,
) -> None:
    order = OrderFactory.create()
    restaurant = RestaurantFactory.create()
    rest_and_order = RestaurantAndOrderFactory.create(
        order=order,
        restaurant=restaurant,
    )
    api_client.force_authenticate(user=waiter.user)
    api_client.delete(
        reverse_lazy(
            "api:restaurantAndOrders-detail",
            kwargs={"pk": rest_and_order.pk},
        ),
    )
    assert not RestaurantAndOrder.objects.filter(
        order=order,
        restaurant=restaurant,
        arrival_time=rest_and_order.arrival_time,
        place_number=rest_and_order.place_number,
    ).exists()
