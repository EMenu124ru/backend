import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.orders.factories import OrderFactory, ReservationFactory
from apps.orders.models import Reservation
from apps.restaurants.factories import PlaceFactory, RestaurantFactory

pytestmark = pytest.mark.django_db


def test_read_list_restaurants_by_manager(
    manager,
    api_client,
) -> None:
    api_client.force_authenticate(user=manager.user)
    response = api_client.get(
        reverse_lazy("api:restaurants-list"),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_list_restaurants_by_client(
    client,
    api_client,
) -> None:
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
        reverse_lazy("api:restaurants-list"),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_state_places_of_restaurant_by_hostess(
    hostess,
    api_client,
):
    restaurant = hostess.restaurant
    api_client.force_authenticate(user=hostess.user)
    response = api_client.get(
        reverse_lazy(
            "api:restaurants-places",
            kwargs={"pk": restaurant.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_state_places_of_restaurant_by_hostess_other_restaurant(
    hostess,
    api_client,
):
    restaurant = RestaurantFactory.create()
    api_client.force_authenticate(user=hostess.user)
    response = api_client.get(
        reverse_lazy(
            "api:restaurants-places",
            kwargs={"pk": restaurant.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_read_state_places_of_restaurant_by_waiter(
    waiter,
    api_client,
):
    restaurant = waiter.restaurant
    api_client.force_authenticate(user=waiter.user)
    response = api_client.get(
        reverse_lazy(
            "api:restaurants-places",
            kwargs={"pk": restaurant.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_state_places_of_restaurant_by_hostess(
    hostess,
    api_client,
):
    places = []
    restaurant = hostess.restaurant
    for i in range(15):
        places.append(PlaceFactory.create(restaurant=restaurant, place=f"A{i}"))
    created_busy, created_reserved, created_free = [], [], []
    for i in range(3):
        reservation = ReservationFactory.create(
            status=Reservation.Statuses.OPENED,
            restaurant=restaurant,
            place=places[i],
        )
        OrderFactory.create(reservation=reservation)
        created_busy.append(i)
    for i in range(3, 6):
        ReservationFactory.create(
            status=Reservation.Statuses.OPENED,
            restaurant=restaurant,
            place=places[i],
        )
        created_reserved.append(i)
    for i in range(6, 9):
        ReservationFactory.create(
            status=Reservation.Statuses.CANCELED,
            restaurant=restaurant,
            place=places[i],
        )
        created_free.append(i)
    for i in range(9, 12):
        ReservationFactory.create(
            status=Reservation.Statuses.FINISHED,
            restaurant=restaurant,
            place=places[i],
        )
        created_free.append(i)
    created_free.extend([12, 13, 14])
    api_client.force_authenticate(user=hostess.user)
    response = api_client.get(
        reverse_lazy(
            "api:restaurants-places",
            kwargs={"pk": restaurant.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK
    free, reserved, busy = response.data["free"], response.data["reserved"], response.data["busy"]
    assert [item["id"] in created_busy for item in busy]
    assert [item["id"] in created_reserved for item in reserved]
    assert [item["id"] in created_free for item in free]


def test_read_tags_of_restaurant_by_hostess(
    hostess,
    api_client,
):
    restaurant = hostess.restaurant
    for i in range(15):
        PlaceFactory.create(restaurant=restaurant, place=f"A{i}")
    api_client.force_authenticate(user=hostess.user)
    response = api_client.get(
        reverse_lazy(
            "api:restaurants-tags",
            kwargs={"pk": restaurant.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_tags_of_restaurant_by_hostess_other_restaurant(
    hostess,
    api_client,
):
    restaurant = RestaurantFactory.create()
    api_client.force_authenticate(user=hostess.user)
    response = api_client.get(
        reverse_lazy(
            "api:restaurants-tags",
            kwargs={"pk": restaurant.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
