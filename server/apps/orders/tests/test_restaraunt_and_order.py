import pytest
from datetime import datetime, timedelta
import pytz
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
    assert RestaurantAndOrder.objects.filter(
        order=new_order.pk,
        restaurant=restaurant.pk,
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


def test_create_rest_and_order_by_client(
    client,
    api_client,
) -> None:
    order = OrderFactory.create()
    restaurant = RestaurantFactory.create()
    rest_and_order = RestaurantAndOrderFactory.build(
        order=order,
        restaurant=restaurant,
    )
    api_client.force_authenticate(user=client.user)
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
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert not RestaurantAndOrder.objects.filter(
        order=order.pk,
        restaurant=restaurant.pk,
        arrival_time=rest_and_order.arrival_time,
        place_number=rest_and_order.place_number,
    ).exists()


def test_update_rest_and_order_by_client(
    client,
    api_client,
) -> None:
    order = OrderFactory.create()
    restaurant = RestaurantFactory.create()
    rest_and_order = RestaurantAndOrderFactory.create(
        order=order,
        restaurant=restaurant,
    )
    new_order = OrderFactory.create()
    api_client.force_authenticate(user=client.user)
    response = api_client.patch(
        reverse_lazy(
            "api:restaurantAndOrders-detail",
            kwargs={"pk": rest_and_order.pk},
        ),
        data={
            "order": new_order,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_remove_rest_and_order_by_client(
    client,
    api_client,
) -> None:
    order = OrderFactory.create()
    restaurant = RestaurantFactory.create()
    rest_and_order = RestaurantAndOrderFactory.create(
        order=order,
        restaurant=restaurant,
    )
    api_client.force_authenticate(user=client.user)
    response = api_client.delete(
        reverse_lazy(
            "api:restaurantAndOrders-detail",
            kwargs={"pk": rest_and_order.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert RestaurantAndOrder.objects.filter(
        order=order,
        restaurant=restaurant,
        arrival_time=rest_and_order.arrival_time,
        place_number=rest_and_order.place_number,
    ).exists()


def test_read_rest_and_order_by_client_success(
    client,
    api_client,
) -> None:
    order = OrderFactory.create(client=client)
    restaurant = RestaurantFactory.create()
    rest_and_order = RestaurantAndOrderFactory.create(
        order=order,
        restaurant=restaurant,
    )
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
        reverse_lazy(
            "api:restaurantAndOrders-detail",
            kwargs={"pk": rest_and_order.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_rest_and_order_by_client_failed(
    client,
    api_client,
) -> None:
    other_client = ClientFactory.create()
    order = OrderFactory.create(client=other_client)
    restaurant = RestaurantFactory.create()
    rest_and_order = RestaurantAndOrderFactory.create(
        order=order,
        restaurant=restaurant,
    )
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
        reverse_lazy(
            "api:restaurantAndOrders-detail",
            kwargs={"pk": rest_and_order.pk},
        ),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_rest_and_order_by_hostess_failed(
    hostess,
    api_client,
) -> None:
    order = OrderFactory.create()
    restaurant = RestaurantFactory.create()
    rest_and_order = RestaurantAndOrderFactory.build(
        order=order,
        restaurant=restaurant,
    )
    api_client.force_authenticate(user=hostess.user)
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
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not RestaurantAndOrder.objects.filter(
        order=order.pk,
        restaurant=restaurant.pk,
        arrival_time=rest_and_order.arrival_time,
        place_number=rest_and_order.place_number,
    ).exists()


def test_create_rest_and_order_by_hostess_success(
    hostess,
    api_client,
) -> None:
    order = None
    restaurant = RestaurantFactory.create()
    rest_and_order = RestaurantAndOrderFactory.build(
        order=order,
        restaurant=restaurant,
    )
    api_client.force_authenticate(user=hostess.user)
    response = api_client.post(
        reverse_lazy("api:restaurantAndOrders-list"),
        data={
            "order": order,
            "restaurant": rest_and_order.restaurant.pk,
            "arrival_time": rest_and_order.arrival_time,
            "place_number": rest_and_order.place_number,
        },
        format='json',
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert RestaurantAndOrder.objects.filter(
        order=order,
        restaurant=restaurant.pk,
        arrival_time=rest_and_order.arrival_time,
        place_number=rest_and_order.place_number,
    ).exists()


def test_update_rest_and_order_by_hostess_failed(
    hostess,
    api_client,
) -> None:
    order = OrderFactory.create()
    restaurant = RestaurantFactory.create()
    rest_and_order = RestaurantAndOrderFactory.create(
        order=order,
        restaurant=restaurant,
    )
    new_order = OrderFactory.create()
    api_client.force_authenticate(user=hostess.user)
    response = api_client.patch(
        reverse_lazy(
            "api:restaurantAndOrders-detail",
            kwargs={"pk": rest_and_order.pk},
        ),
        data={
            "order": new_order,
        },
    )
    # эмм пишет, что все норм поменялось, так не должно быть
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert RestaurantAndOrder.objects.filter(
        order=order,
        restaurant=restaurant,
        arrival_time=rest_and_order.arrival_time,
        place_number=rest_and_order.place_number,
    ).exists()


def test_update_rest_and_order_by_hostess_success(
    hostess,
    api_client,
) -> None:
    order = OrderFactory.create()
    restaurant = RestaurantFactory.create()
    rest_and_order = RestaurantAndOrderFactory.create(
        order=order,
        restaurant=restaurant,
    )
    new_arrival_time = datetime.now(pytz.UTC) + timedelta(days=3)
    api_client.force_authenticate(user=hostess.user)
    response = api_client.patch(
        reverse_lazy(
            "api:restaurantAndOrders-detail",
            kwargs={"pk": rest_and_order.pk},
        ),
        data={
            "arrival_time": new_arrival_time,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert RestaurantAndOrder.objects.filter(
        order=order,
        restaurant=restaurant,
        arrival_time=new_arrival_time,
        place_number=rest_and_order.place_number,
    ).exists()


def test_create_rest_and_order_by_unauthorised(
    api_client,
) -> None:
    order = OrderFactory.build()
    restaurant = RestaurantFactory.build()
    rest_and_order = RestaurantAndOrderFactory.build(
        order=order,
        restaurant=restaurant,
    )
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
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert not RestaurantAndOrder.objects.filter(
        order=order.pk,
        restaurant=restaurant.pk,
        arrival_time=rest_and_order.arrival_time,
        place_number=rest_and_order.place_number,
    ).exists()


def test_read_rest_and_order_by_unauthorised(
    api_client,
) -> None:
    order = OrderFactory.create()
    restaurant = RestaurantFactory.create()
    rest_and_order = RestaurantAndOrderFactory.create(
        order=order,
        restaurant=restaurant,
    )
    response = api_client.get(
        reverse_lazy(
            "api:restaurantAndOrders-detail",
            kwargs={"pk": rest_and_order.pk},
        ),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_rest_and_order_by_unauthorised(
    api_client,
) -> None:
    order = OrderFactory.create()
    restaurant = RestaurantFactory.create()
    rest_and_order = RestaurantAndOrderFactory.create(
        order=order,
        restaurant=restaurant,
    )
    new_order = OrderFactory.create()
    response = api_client.patch(
        reverse_lazy(
            "api:restaurantAndOrders-detail",
            kwargs={"pk": rest_and_order.pk},
        ),
        data={
            "order": new_order,
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_remove_rest_and_order_by_unauthorised(
    api_client,
) -> None:
    order = OrderFactory.create()
    restaurant = RestaurantFactory.create()
    rest_and_order = RestaurantAndOrderFactory.create(
        order=order,
        restaurant=restaurant,
    )
    response = api_client.delete(
        reverse_lazy(
            "api:restaurantAndOrders-detail",
            kwargs={"pk": rest_and_order.pk},
        ),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
