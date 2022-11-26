import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.orders.factories import CategoryFactory, DishFactory
from apps.orders.models import Dish

pytestmark = pytest.mark.django_db

DISH_COUNT = 3


def test_create_dish_by_manager(
    manager,
    api_client,
) -> None:
    dish = DishFactory.build()
    category = CategoryFactory.create()
    api_client.force_authenticate(user=manager.user)
    response = api_client.post(
        reverse_lazy("api:dishes-list"),
        data={
            "category": category.pk,
            "name": dish.name,
            "description": dish.description,
            "short_description": dish.short_description,
            "compound": dish.compound,
            "weight": dish.weight,
            "price": dish.price,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Dish.objects.filter(
        category=category.pk,
        name=dish.name,
        description=dish.description,
        short_description=dish.short_description,
        compound=dish.compound,
        weight=dish.weight,
        price=dish.price,
    ).exists()


def test_update_dish_by_manager(
    manager,
    api_client,
) -> None:
    dish = DishFactory.create()
    api_client.force_authenticate(user=manager.user)
    new_name = "New name"
    response = api_client.patch(
        reverse_lazy(
            "api:dishes-detail",
            kwargs={"pk": dish.pk},
        ),
        data={
            "name": new_name,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert Dish.objects.filter(
        id=dish.pk,
        name=new_name,
    ).exists()


def test_read_dishes_by_manager(
    manager,
    api_client,
) -> None:
    DishFactory.create_batch(
        size=DISH_COUNT,
    )
    api_client.force_authenticate(user=manager.user)
    response = api_client.get(
        reverse_lazy("api:dishes-list"),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_dish_orders_by_manager(
    manager,
    api_client,
) -> None:
    dish = DishFactory.create()
    api_client.force_authenticate(user=manager.user)
    response = api_client.get(
        reverse_lazy(
            "api:dishes-orders",
            kwargs={"pk": dish.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK


# def test_read_dish_reviews_by_manager(
#     manager,
#     api_client,
# ) -> None:
#     DishFactory.create_batch(
#         size=DISH_COUNT,
#     )
#     api_client.force_authenticate(user=manager.user)
#     response = api_client.get(
#         reverse_lazy(
#             "api:dishes-reviews",
#             kwargs={"pk": dish.pk},
#         ),
#     )
#     assert response.status_code == status.HTTP_200_OK


def test_read_dish_by_manager(
    manager,
    api_client,
) -> None:
    dish = DishFactory.create()
    api_client.force_authenticate(user=manager.user)
    response = api_client.get(
        reverse_lazy(
            "api:dishes-detail",
            kwargs={"pk": dish.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_remove_dish_by_manager(
    manager,
    api_client,
) -> None:
    dish = DishFactory.create()
    api_client.force_authenticate(user=manager.user)
    api_client.delete(
        reverse_lazy(
            "api:dishes-detail",
            kwargs={"pk": dish.pk},
        ),
    )
    assert dish not in Dish.objects.all()


def test_create_dish_by_client(
    client,
    api_client,
) -> None:
    dish = DishFactory.build()
    category = CategoryFactory.create()
    api_client.force_authenticate(user=client.user)
    response = api_client.post(
        reverse_lazy("api:dishes-list"),
        data={
            "category": category.pk,
            "name": dish.name,
            "description": dish.description,
            "short_description": dish.short_description,
            "compound": dish.compound,
            "weight": dish.weight,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_dish_by_client(
    client,
    api_client,
) -> None:
    dish = DishFactory.create()
    api_client.force_authenticate(user=client.user)
    new_name = "New name"
    response = api_client.patch(
        reverse_lazy(
            "api:dishes-detail",
            kwargs={"pk": dish.pk},
        ),
        data={
            "name": new_name,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_read_dishes_by_client(
    client,
    api_client,
) -> None:
    DishFactory.create_batch(
        size=DISH_COUNT,
    )
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
        reverse_lazy(
            "api:dishes-list",
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_dish_orders_by_client(
    client,
    api_client,
) -> None:
    dish = DishFactory.create()
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
        reverse_lazy(
            "api:dishes-orders",
            kwargs={"pk": dish.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


# def test_read_dish_reviews_by_client(
#     client,
#     api_client,
# ) -> None:
#     DishFactory.create_batch(
#         size=DISH_COUNT,
#     )
#     api_client.force_authenticate(user=client.user)
#     response = api_client.get(
#         reverse_lazy(
#             "api:dishes-reviews",
#             kwargs={"pk": dish.pk},
#         ),
#     )
#     assert response.status_code == status.HTTP_200_OK


def test_read_dish_by_client(
    client,
    api_client,
) -> None:
    dish = DishFactory.create()
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
        reverse_lazy(
            "api:dishes-detail",
            kwargs={"pk": dish.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_remove_dish_by_client(
    client,
    api_client,
) -> None:
    dish = DishFactory.create()
    api_client.force_authenticate(user=client.user)
    response = api_client.delete(
        reverse_lazy(
            "api:dishes-detail",
            kwargs={"pk": dish.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_dish_by_not_auth(
    api_client,
) -> None:
    dish = DishFactory.build()
    category = CategoryFactory.create()
    response = api_client.post(
        reverse_lazy("api:dishes-list"),
        data={
            "category": category.pk,
            "name": dish.name,
            "description": dish.description,
            "short_description": dish.short_description,
            "compound": dish.compound,
            "weight": dish.weight,
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_dish_by_not_auth(
    api_client,
) -> None:
    dish = DishFactory.create()
    new_name = "New name"
    response = api_client.patch(
        reverse_lazy(
            "api:dishes-detail",
            kwargs={"pk": dish.pk},
        ),
        data={
            "name": new_name,
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_read_dishes_by_not_auth(
    api_client,
) -> None:
    DishFactory.create_batch(
        size=DISH_COUNT,
    )
    response = api_client.get(
        reverse_lazy(
            "api:dishes-list",
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_dish_orders_by_not_auth(
    api_client,
) -> None:
    dish = DishFactory.create()
    response = api_client.get(
        reverse_lazy(
            "api:dishes-orders",
            kwargs={"pk": dish.pk},
        ),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# def test_read_dish_reviews_by_not_auth(
#     api_client,
# ) -> None:
#     DishFactory.create_batch(
#         size=DISH_COUNT,
#     )
#     response = api_client.get(
#         reverse_lazy(
#             "api:dishes-reviews",
#             kwargs={"pk": dish.pk},
#         ),
#     )
#     assert response.status_code == status.HTTP_200_OK


def test_read_dish_by_not_auth(
    api_client,
) -> None:
    dish = DishFactory.create()
    response = api_client.get(
        reverse_lazy(
            "api:dishes-detail",
            kwargs={"pk": dish.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_remove_dish_by_not_auth(
    api_client,
) -> None:
    dish = DishFactory.create()
    response = api_client.delete(
        reverse_lazy(
            "api:dishes-detail",
            kwargs={"pk": dish.pk},
        ),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
