import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.orders.factories import DishFactory, DishImagesFactory
from apps.orders.models import Dish, DishImages

pytestmark = pytest.mark.django_db

COUNT_IMAGES = 2


def test_create_dish_images_by_manager(
    manager,
    api_client,
) -> None:
    dish = DishFactory.create()
    dish_images = DishImagesFactory.build_batch(size=COUNT_IMAGES)
    data = {
        "images": [image.image for image in dish_images],
        "dish": dish.pk,
    }
    api_client.force_authenticate(user=manager.user)
    response = api_client.post(
        reverse_lazy("api:dish-images-list"),
        data=data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert DishImages.objects.filter(dish__id=dish.id).exists()
    assert DishImages.objects.filter(dish__id=dish.id).count() == COUNT_IMAGES


def test_delete_dish_images_by_manager(
    manager,
    api_client,
) -> None:
    dish = DishFactory.create()
    dish_images = DishImagesFactory.create_batch(size=COUNT_IMAGES, dish=dish)
    api_client.force_authenticate(user=manager.user)
    for image in dish_images:
        api_client.delete(
            reverse_lazy(
                "api:dish-images-detail",
                kwargs={"pk": image.pk},
            ),
        )
    assert not DishImages.objects.filter(
        id__in=[image.id for image in dish_images]
    ).exists()
    assert not Dish.objects.get(id=dish.id).images.all().exists()


def test_create_dish_images_by_waiter(
    waiter,
    api_client,
) -> None:
    dish = DishFactory.create()
    dish_images = DishImagesFactory.build_batch(size=COUNT_IMAGES)
    data = {
        "images": [image.image for image in dish_images],
        "dish": dish.id,
    }
    api_client.force_authenticate(user=waiter.user)
    response = api_client.post(
        reverse_lazy("api:dish-images-list"),
        data=data,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_dish_images_by_waiter(
    waiter,
    api_client,
) -> None:
    dish = DishFactory.create()
    dish_images = DishImagesFactory.create_batch(size=COUNT_IMAGES, dish=dish)
    api_client.force_authenticate(user=waiter.user)
    for image in dish_images:
        api_client.delete(
            reverse_lazy(
                "api:dish-images-detail",
                kwargs={"pk": image.pk},
            ),
        )
    assert DishImages.objects.filter(
        id__in=[image.id for image in dish_images]
    ).exists()
    assert Dish.objects.get(id=dish.id).images.all().exists()


def test_create_dish_images_by_client(
    client,
    api_client,
) -> None:
    dish = DishFactory.create()
    dish_images = DishImagesFactory.build_batch(size=COUNT_IMAGES)
    data = {
        "images": [image.image for image in dish_images],
        "dish": dish.id,
    }
    api_client.force_authenticate(user=client.user)
    response = api_client.post(
        reverse_lazy("api:dish-images-list"),
        data=data,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_dish_images_by_client(
    client,
    api_client,
) -> None:
    dish = DishFactory.create()
    dish_images = DishImagesFactory.create_batch(size=COUNT_IMAGES, dish=dish)
    api_client.force_authenticate(user=client.user)
    for image in dish_images:
        api_client.delete(
            reverse_lazy(
                "api:dish-images-detail",
                kwargs={"pk": image.pk},
            ),
        )
    assert DishImages.objects.filter(
        id__in=[image.id for image in dish_images]
    ).exists()
    assert Dish.objects.get(id=dish.id).images.all().exists()


def test_create_dish_images_by_not_auth(
    api_client,
) -> None:
    dish = DishFactory.create()
    dish_images = DishImagesFactory.build_batch(size=COUNT_IMAGES)
    data = {
        "images": [image.image for image in dish_images],
        "dish": dish.id,
    }
    response = api_client.post(
        reverse_lazy("api:dish-images-list"),
        data=data,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_dish_images_by_not_auth(
    api_client,
) -> None:
    dish = DishFactory.create()
    dish_images = DishImagesFactory.create_batch(size=COUNT_IMAGES, dish=dish)
    for image in dish_images:
        api_client.delete(
            reverse_lazy(
                "api:dish-images-detail",
                kwargs={"pk": image.pk},
            ),
        )
    assert DishImages.objects.filter(
        id__in=[image.id for image in dish_images]
    ).exists()
    assert Dish.objects.get(id=dish.id).images.all().exists()
