import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.orders.factories import CategoryFactory
from apps.orders.models import Category

pytestmark = pytest.mark.django_db

COUNT_CATEGORIES = 3


def test_create_category_by_manager(
    manager,
    api_client,
) -> None:
    category = CategoryFactory.build()
    api_client.force_authenticate(user=manager.user)
    response = api_client.post(
        reverse_lazy("api:categories-list"),
        data={
            "name": category.name,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Category.objects.filter(
        name=category.name,
    ).exists()


def test_update_category_by_manager(
    manager,
    api_client,
) -> None:
    category = CategoryFactory.create()
    api_client.force_authenticate(user=manager.user)
    new_name = "New name"
    response = api_client.put(
        reverse_lazy(
            "api:categories-detail",
            kwargs={"pk": category.pk},
        ),
        data={
            "name": new_name,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert Category.objects.filter(
        id=category.pk,
        name=new_name,
    ).exists()


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


def test_remove_category_by_manager(
    manager,
    api_client,
) -> None:
    category = CategoryFactory.create()
    api_client.force_authenticate(user=manager.user)
    api_client.delete(
        reverse_lazy(
            "api:categories-detail",
            kwargs={"pk": category.pk},
        ),
    )
    assert category not in Category.objects.all()


def test_create_category_by_client(
    client,
    api_client,
) -> None:
    category = CategoryFactory.build()
    api_client.force_authenticate(user=client.user)
    response = api_client.post(
        reverse_lazy("api:categories-list"),
        data={
            "name": category.name,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_category_by_client(
    client,
    api_client,
) -> None:
    category = CategoryFactory.create()
    api_client.force_authenticate(user=client.user)
    new_name = "New name"
    response = api_client.put(
        reverse_lazy(
            "api:categories-detail",
            kwargs={"pk": category.pk},
        ),
        data={
            "name": new_name,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


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


def test_remove_category_by_client(
    client,
    api_client,
) -> None:
    category = CategoryFactory.create()
    api_client.force_authenticate(user=client.user)
    response = api_client.delete(
        reverse_lazy(
            "api:categories-detail",
            kwargs={"pk": category.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_category_by_not_auth(
    api_client,
) -> None:
    category = CategoryFactory.build()
    response = api_client.post(
        reverse_lazy("api:categories-list"),
        data={
            "name": category.name,
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_category_by_not_auth(
    api_client,
) -> None:
    category = CategoryFactory.create()
    new_name = "New name"
    response = api_client.put(
        reverse_lazy(
            "api:categories-detail",
            kwargs={"pk": category.pk},
        ),
        data={
            "name": new_name,
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


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


def test_remove_category_by_not_auth(
    api_client,
) -> None:
    category = CategoryFactory.create()
    response = api_client.delete(
        reverse_lazy(
            "api:categories-detail",
            kwargs={"pk": category.pk},
        ),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
