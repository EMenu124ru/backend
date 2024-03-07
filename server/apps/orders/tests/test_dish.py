import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.orders.factories import DishFactory, IngredientFactory

pytestmark = pytest.mark.django_db

DISH_COUNT = INGREDIENT_COUNT = 3
DISH_IMAGES_COUNT = 5


def test_read_ingredients_by_manager(
    manager,
    api_client,
) -> None:
    IngredientFactory.create_batch(size=INGREDIENT_COUNT)
    api_client.force_authenticate(user=manager.user)
    response = api_client.get(
        reverse_lazy("api:ingredients-list"),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_read_ingredients_by_chef(
    chef,
    api_client,
) -> None:
    IngredientFactory.create_batch(size=INGREDIENT_COUNT)
    api_client.force_authenticate(user=chef.user)
    response = api_client.get(
        reverse_lazy("api:ingredients-list"),
    )
    assert response.status_code == status.HTTP_200_OK


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


def test_read_ingredients_by_client(
    client,
    api_client,
) -> None:
    IngredientFactory.create_batch(size=INGREDIENT_COUNT)
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
        reverse_lazy("api:ingredients-list"),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


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


def test_read_ingredients_by_not_auth(
    api_client,
) -> None:
    IngredientFactory.create_batch(size=INGREDIENT_COUNT)
    response = api_client.get(
        reverse_lazy("api:ingredients-list"),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


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
