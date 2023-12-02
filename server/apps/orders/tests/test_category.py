import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.orders.factories import CategoryFactory

pytestmark = pytest.mark.django_db

COUNT_CATEGORIES = 3


def test_read_categories_by_manager(
    manager,
    api_client,
) -> None:
    CategoryFactory.create_batch(size=COUNT_CATEGORIES)
    api_client.force_authenticate(user=manager.user)
    response = api_client.get(
        reverse_lazy("api:categories-list"),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_category_dishes_by_manager(
    manager,
    api_client,
) -> None:
    category = CategoryFactory.create()
    api_client.force_authenticate(user=manager.user)
    response = api_client.get(
        reverse_lazy(
            "api:categories-dishes",
            kwargs={"pk": category.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_category_by_manager(
    manager,
    api_client,
) -> None:
    category = CategoryFactory.create()
    api_client.force_authenticate(user=manager.user)
    response = api_client.get(
        reverse_lazy(
            "api:categories-detail",
            kwargs={"pk": category.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_categories_by_client(
    client,
    api_client,
) -> None:
    CategoryFactory.create_batch(size=COUNT_CATEGORIES)
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
        reverse_lazy(
            "api:categories-list",
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_category_dishes_by_client(
    client,
    api_client,
) -> None:
    category = CategoryFactory.create()
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
        reverse_lazy(
            "api:categories-dishes",
            kwargs={"pk": category.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_category_by_client(
    client,
    api_client,
) -> None:
    category = CategoryFactory.create()
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
        reverse_lazy(
            "api:categories-detail",
            kwargs={"pk": category.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_categories_by_not_auth(
    api_client,
) -> None:
    CategoryFactory.create_batch(size=COUNT_CATEGORIES)
    response = api_client.get(
        reverse_lazy(
            "api:categories-list",
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_category_dishes_by_not_auth(
    api_client,
) -> None:
    category = CategoryFactory.create()
    response = api_client.get(
        reverse_lazy(
            "api:categories-dishes",
            kwargs={"pk": category.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_category_by_not_auth(
    api_client,
) -> None:
    category = CategoryFactory.create()
    response = api_client.get(
        reverse_lazy(
            "api:categories-detail",
            kwargs={"pk": category.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK
