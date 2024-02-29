import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.orders.factories import OrderFactory, ReservationFactory
from apps.orders.models import Reservation
from apps.restaurants.factories import PlaceFactory

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
    api_client.force_authenticate(user=hostess.user)
    response = api_client.get(
        reverse_lazy(
            "api:restaurants-places",
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_state_places_of_restaurant_by_waiter(
    waiter,
    api_client,
):
    api_client.force_authenticate(user=waiter.user)
    response = api_client.get(
        reverse_lazy(
            "api:restaurants-places",
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_state_places_of_restaurant_by_hostess(
    hostess,
    api_client,
):
    places = []
    restaurant = hostess.restaurant
    restaurant.places.all().delete()
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
        created_busy.append(places[i].pk)
    for i in range(3, 6):
        ReservationFactory.create(
            status=Reservation.Statuses.OPENED,
            restaurant=restaurant,
            place=places[i],
        )
        created_reserved.append(places[i].pk)
    for i in range(6, 9):
        ReservationFactory.create(
            status=Reservation.Statuses.CANCELED,
            restaurant=restaurant,
            place=places[i],
        )
        created_free.append(places[i].pk)
    for i in range(9, 12):
        ReservationFactory.create(
            status=Reservation.Statuses.FINISHED,
            restaurant=restaurant,
            place=places[i],
        )
        created_free.append(places[i].pk)
    for i in range(12, 15):
        created_free.append(places[i].pk)
    api_client.force_authenticate(user=hostess.user)
    response = api_client.get(
        reverse_lazy(
            "api:restaurants-places",
        ),
    )
    assert response.status_code == status.HTTP_200_OK
    free, reserved, busy = response.data["free"], response.data["reserved"], response.data["busy"]
    assert len(busy) == 3 and all([item["id"] in created_busy for item in busy])
    assert len(reserved) == 3 and all([item["id"] in created_reserved for item in reserved])
    assert len(free) == 9 and all([item["id"] in created_free for item in free])


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
        ),
    )
    assert response.status_code == status.HTTP_200_OK
