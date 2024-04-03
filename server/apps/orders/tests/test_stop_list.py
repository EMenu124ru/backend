import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.orders.factories import (
    CategoryFactory,
    DishFactory,
    IngredientFactory,
    StopListFactory,
)
from apps.orders.models import StopList
from apps.restaurants.factories import RestaurantFactory

pytestmark = pytest.mark.django_db
DISH_COUNT = 6


def test_create_stop_list_by_manager(
    manager,
    api_client,
) -> None:
    ingredient = IngredientFactory.create()
    api_client.force_authenticate(user=manager.user)
    response = api_client.post(
        reverse_lazy("api:stopList-list"),
        data={
            "ingredient": ingredient.pk,
            "restaurant": manager.restaurant.pk,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert not StopList.objects.filter(
        ingredient=ingredient.pk,
        restaurant=manager.restaurant,
    ).exists()


def test_read_stop_list_by_manager(
    manager,
    api_client,
) -> None:
    api_client.force_authenticate(user=manager.user)
    response = api_client.get(
        reverse_lazy("api:stopList-list"),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_remove_stop_list_by_manager(
    manager,
    api_client,
) -> None:
    stop_list = StopListFactory.create(restaurant=manager.restaurant)
    api_client.force_authenticate(user=manager.user)
    response = api_client.delete(
        reverse_lazy(
            "api:stopList-detail",
            kwargs={"pk": stop_list.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert StopList.objects.filter(id=stop_list.pk).exists()


def test_create_stop_list_by_chef(
    chef,
    api_client,
) -> None:
    ingredient = IngredientFactory.create()
    api_client.force_authenticate(user=chef.user)
    response = api_client.post(
        reverse_lazy("api:stopList-list"),
        data={
            "ingredient": ingredient.pk,
            "restaurant": chef.restaurant.pk,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert StopList.objects.filter(
        ingredient=ingredient.pk,
        restaurant=chef.restaurant,
    ).exists()


def test_read_stop_lists_by_chef(
    chef,
    api_client,
) -> None:
    api_client.force_authenticate(user=chef.user)
    response = api_client.get(
        reverse_lazy("api:stopList-list"),
    )
    assert response.status_code == status.HTTP_200_OK


def test_remove_stop_list_by_chef(
    chef,
    api_client,
) -> None:
    stop_list = StopListFactory.create(restaurant=chef.restaurant)
    api_client.force_authenticate(user=chef.user)
    response = api_client.delete(
        reverse_lazy(
            "api:stopList-detail",
            kwargs={"pk": stop_list.pk},
        ),
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not StopList.objects.filter(id=stop_list.pk).exists()


def test_create_stop_list_by_waiter(
    waiter,
    api_client,
) -> None:
    ingredient = IngredientFactory.create()
    restaurant = RestaurantFactory.create()
    api_client.force_authenticate(user=waiter.user)
    response = api_client.post(
        reverse_lazy("api:stopList-list"),
        data={
            "ingredient": ingredient.pk,
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
            "ingredient": IngredientFactory.create().pk,
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
    ingredient = IngredientFactory.create()
    restaurant = RestaurantFactory.create()
    api_client.force_authenticate(user=client.user)
    response = api_client.post(
        reverse_lazy("api:stopList-list"),
        data={
            "ingredient": ingredient.pk,
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
            "ingredient": IngredientFactory.create().pk,
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
    ingredient = IngredientFactory.create()
    restaurant = RestaurantFactory.create()
    response = api_client.post(
        reverse_lazy("api:stopList-list"),
        data={
            "ingredient": ingredient.pk,
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
            "ingredient": IngredientFactory.create().pk,
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


def test_read_dish_apply_stop_list(
    waiter,
    api_client,
) -> None:
    category = CategoryFactory.create()
    dishes = DishFactory.create_batch(
        category=category,
        size=DISH_COUNT,
    )
    ingredients = IngredientFactory.create_batch(
        size=DISH_COUNT * 2,
    )
    count_access_dishes = DISH_COUNT
    access_to_dish = []
    broke_ingredients = []
    ingredients = [
        (ingredients[i], ingredients[i+1])
        for i in range(0, len(ingredients), 2)
    ]
    for index, dish in enumerate(dishes):
        dish_ingredients = ingredients[index]
        dish.ingredients.clear()
        dish.ingredients.set(ingredients[index])
        if (
            dish_ingredients[0].id in broke_ingredients or
            dish_ingredients[1].id in broke_ingredients
        ):
            count_access_dishes -= 1
            continue
        if index % 2 == 0:
            for ingredient in dish.ingredients.all():
                if ingredient.id not in broke_ingredients:
                    broke_ingredients.append(ingredient.id)
                    StopListFactory.create(
                        ingredient=ingredient,
                        restaurant=waiter.restaurant,
                    )
                    count_access_dishes -= 1
                    break
        else:
            access_to_dish.append(dish.id)
    api_client.force_authenticate(user=waiter.user)
    response = api_client.get(
        reverse_lazy(
            "api:categories-dishes",
            kwargs={"pk": category.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == len(access_to_dish)
    access_dishes = [dish["id"] for dish in response.data["results"]]
    assert sorted(access_to_dish) == sorted(access_dishes)
