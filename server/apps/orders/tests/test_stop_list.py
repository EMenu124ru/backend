import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.orders.factories import DishFactory, StopListFactory
from apps.orders.models import StopList
from apps.restaurants.factories import RestaurantFactory

pytestmark = pytest.mark.django_db


def test_create_stop_list_by_cook(
    cook,
    api_client,
) -> None:
    dish = DishFactory.create()
    restaurant = RestaurantFactory.create()
    api_client.force_authenticate(user=cook.user)
    response = api_client.post(
        reverse_lazy("api:stopList-list"),
        data={
            "dish": dish.pk,
            "restaurant": restaurant.pk,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert StopList.objects.filter(
        dish=dish,
        restaurant=restaurant,
    ).exists()


def test_read_stop_lists_by_cook(
    cook,
    api_client,
) -> None:
    api_client.force_authenticate(user=cook.user)
    response = api_client.get(
        reverse_lazy("api:stopList-list"),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_stop_list_by_cook(
    cook,
    api_client,
) -> None:
    stop_list = StopListFactory.create()
    api_client.force_authenticate(user=cook.user)
    response = api_client.get(
        reverse_lazy(
            "api:stopList-detail",
            kwargs={"pk": stop_list.pk},
        ),
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_update_stop_list_by_cook(
    cook,
    api_client,
) -> None:
    stop_list = StopListFactory.create()
    api_client.force_authenticate(user=cook.user)
    response = api_client.patch(
        reverse_lazy(
            "api:stopList-detail",
            kwargs={"pk": stop_list.pk},
        ),
        data={
            "dish": DishFactory.create().pk,
        },
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_remove_stop_list_by_cook(
    cook,
    api_client,
) -> None:
    stop_list = StopListFactory.create()
    api_client.force_authenticate(user=cook.user)
    api_client.delete(
        reverse_lazy(
            "api:stopList-detail",
            kwargs={"pk": stop_list.pk},
        ),
    )
    assert not StopList.objects.filter(id=stop_list.pk).exists()


def test_create_stop_list_by_waiter(
    waiter,
    api_client,
) -> None:
    dish = DishFactory.create()
    restaurant = RestaurantFactory.create()
    api_client.force_authenticate(user=waiter.user)
    response = api_client.post(
        reverse_lazy("api:stopList-list"),
        data={
            "dish": dish.pk,
            "restaurant": restaurant.pk,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_read_stop_lists_by_waiter(
    waiter,
    api_client,
) -> None:
    api_client.force_authenticate(user=waiter.user)
    response = api_client.get(
        reverse_lazy("api:stopList-list"),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_stop_list_by_waiter(
    waiter,
    api_client,
) -> None:
    stop_list = StopListFactory.create()
    api_client.force_authenticate(user=waiter.user)
    response = api_client.get(
        reverse_lazy(
            "api:stopList-detail",
            kwargs={"pk": stop_list.pk},
        ),
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_update_stop_list_by_waiter(
    waiter,
    api_client,
) -> None:
    stop_list = StopListFactory.create()
    api_client.force_authenticate(user=waiter.user)
    response = api_client.patch(
        reverse_lazy(
            "api:stopList-detail",
            kwargs={"pk": stop_list.pk},
        ),
        data={
            "dish": DishFactory.create().pk,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_remove_stop_list_by_waiter(
    waiter,
    api_client,
) -> None:
    stop_list = StopListFactory.create()
    api_client.force_authenticate(user=waiter.user)
    response = api_client.delete(
        reverse_lazy(
            "api:stopList-detail",
            kwargs={"pk": stop_list.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert StopList.objects.filter(id=stop_list.pk).exists()


def test_create_stop_list_by_client(
    client,
    api_client,
) -> None:
    dish = DishFactory.create()
    restaurant = RestaurantFactory.create()
    api_client.force_authenticate(user=client.user)
    response = api_client.post(
        reverse_lazy("api:stopList-list"),
        data={
            "dish": dish.pk,
            "restaurant": restaurant.pk,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_read_stop_lists_by_client(
    client,
    api_client,
) -> None:
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
        reverse_lazy("api:stopList-list"),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_read_stop_list_by_client(
    client,
    api_client,
) -> None:
    stop_list = StopListFactory.create()
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
        reverse_lazy(
            "api:stopList-detail",
            kwargs={"pk": stop_list.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_stop_list_by_client(
    client,
    api_client,
) -> None:
    stop_list = StopListFactory.create()
    api_client.force_authenticate(user=client.user)
    response = api_client.patch(
        reverse_lazy(
            "api:stopList-detail",
            kwargs={"pk": stop_list.pk},
        ),
        data={
            "dish": DishFactory.create().pk,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_remove_stop_list_by_client(
    client,
    api_client,
) -> None:
    stop_list = StopListFactory.create()
    api_client.force_authenticate(user=client.user)
    response = api_client.delete(
        reverse_lazy(
            "api:stopList-detail",
            kwargs={"pk": stop_list.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_stop_list_by_not_auth(
    api_client,
) -> None:
    dish = DishFactory.create()
    restaurant = RestaurantFactory.create()
    response = api_client.post(
        reverse_lazy("api:stopList-list"),
        data={
            "dish": dish.pk,
            "restaurant": restaurant.pk,
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_read_stop_lists_by_not_auth(
    api_client,
) -> None:
    response = api_client.get(
        reverse_lazy("api:stopList-list"),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_read_stop_list_by_not_auth(
    api_client,
) -> None:
    stop_list = StopListFactory.create()
    response = api_client.get(
        reverse_lazy(
            "api:stopList-detail",
            kwargs={"pk": stop_list.pk},
        ),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_stop_list_by_not_auth(
    api_client,
) -> None:
    stop_list = StopListFactory.create()
    response = api_client.patch(
        reverse_lazy(
            "api:stopList-detail",
            kwargs={"pk": stop_list.pk},
        ),
        data={
            "dish": DishFactory.create().pk,
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_stop_list_by_not_auth(
    api_client,
) -> None:
    stop_list = StopListFactory.create()
    response = api_client.delete(
        reverse_lazy(
            "api:stopList-detail",
            kwargs={"pk": stop_list.pk},
        ),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
