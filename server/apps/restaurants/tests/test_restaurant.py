import pytest
from django.urls import reverse_lazy
from rest_framework import status

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
