import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.restaurants.factories import RestaurantFactory

pytestmark = pytest.mark.django_db


def test_read_restaurant_by_manager(
    manager,
    api_client,
) -> None:
    restaurant = RestaurantFactory.create()
    api_client.force_authenticate(user=manager.user)
    response = api_client.get(
        reverse_lazy(
            "api:restaurants-detail",
            kwargs={"pk": restaurant.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_list_restaurants_by_manager(
    manager,
    api_client,
) -> None:
    api_client.force_authenticate(user=manager.user)
    response = api_client.get(
        reverse_lazy("api:restaurants-list"),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_restaurant_by_client(
    client,
    api_client,
) -> None:
    restaurant = RestaurantFactory.create()
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
        reverse_lazy(
            "api:restaurants-detail",
            kwargs={"pk": restaurant.pk},
        ),
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


def test_read_restaurant_by_not_auth_user(
    api_client,
) -> None:
    restaurant = RestaurantFactory.create()
    response = api_client.get(
        reverse_lazy(
            "api:restaurants-detail",
            kwargs={"pk": restaurant.pk},
        ),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_read_list_restaurants_by_not_auth_user(
    api_client,
) -> None:
    response = api_client.get(
        reverse_lazy("api:restaurants-list"),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_read_reviews_of_restaurant_by_client(
    client,
    api_client,
) -> None:
    restaurant = RestaurantFactory.create()
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
        reverse_lazy(
            "api:restaurants-reviews",
            kwargs={"pk": restaurant.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_reviews_of_restaurant_by_not_auth_user(
    api_client,
) -> None:
    restaurant = RestaurantFactory.create()
    response = api_client.get(
        reverse_lazy(
            "api:restaurants-reviews",
            kwargs={"pk": restaurant.pk},
        ),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_read_reviews_of_restaurant_by_manager(
    manager,
    api_client,
) -> None:
    restaurant = RestaurantFactory.create()
    api_client.force_authenticate(user=manager.user)
    response = api_client.get(
        reverse_lazy(
            "api:restaurants-reviews",
            kwargs={"pk": restaurant.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK
