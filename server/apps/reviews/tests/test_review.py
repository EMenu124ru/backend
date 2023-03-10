from decimal import Decimal

import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.orders.factories import DishFactory
from apps.reviews.factories import ReviewFactory, ReviewImageFactory
from apps.reviews.models import Review

pytestmark = pytest.mark.django_db

REVIEW_COUNT = 3
REVIEW_IMAGES_COUNT = 5


def test_create_review_by_manager(
    manager,
    api_client,
) -> None:
    review = ReviewFactory.build()
    api_client.force_authenticate(user=manager.user)
    response = api_client.post(
        reverse_lazy("api:reviews-list"),
        data={
            "review": review.review,
            "mark": review.mark,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_review_by_manager(
    manager,
    api_client,
) -> None:
    review = ReviewFactory.create()
    api_client.force_authenticate(user=manager.user)
    new_mark = Decimal("3.0")
    response = api_client.patch(
        reverse_lazy(
            "api:reviews-detail",
            kwargs={"pk": review.pk},
        ),
        data={
            "mark": new_mark,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_read_review_by_manager(
    manager,
    api_client,
) -> None:
    review = ReviewFactory.create()
    api_client.force_authenticate(user=manager.user)
    response = api_client.get(
        reverse_lazy(
            "api:reviews-detail",
            kwargs={"pk": review.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_remove_review_by_manager(
    manager,
    api_client,
) -> None:
    review = ReviewFactory.create()
    api_client.force_authenticate(user=manager.user)
    response = api_client.delete(
        reverse_lazy(
            "api:reviews-detail",
            kwargs={"pk": review.pk},
        ),
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert review not in Review.objects.all()


def test_create_review_by_client_without_images(
    client,
    api_client,
) -> None:
    review = ReviewFactory.build()
    dish = DishFactory.create()
    api_client.force_authenticate(user=client.user)
    response = api_client.post(
        reverse_lazy("api:reviews-list"),
        data={
            "review": review.review,
            "mark": review.mark,
            "dish": dish.pk,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Review.objects.filter(
        review=review.review,
        mark=review.mark,
        client=client.pk,
    ).exists()


def test_create_review_by_client_with_images(
    client,
    api_client,
) -> None:
    review = ReviewFactory.build()
    dish = DishFactory.create()
    review_images = ReviewImageFactory.build_batch(size=REVIEW_IMAGES_COUNT)
    images = [review_image.image for review_image in review_images]
    api_client.force_authenticate(user=client.user)
    response = api_client.post(
        reverse_lazy("api:reviews-list"),
        data={
            "review": review.review,
            "mark": review.mark,
            "images": images,
            "dish": dish.pk,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Review.objects.filter(
        review=review.review,
        mark=review.mark,
        client=client.pk,
    ).exists()
    assert Review.objects.get(
        review=review.review,
        mark=review.mark,
        client=client.pk,
    ).images.count() == REVIEW_IMAGES_COUNT


def test_update_review_by_client(
    client,
    api_client,
) -> None:
    review = ReviewFactory.create(client=client)
    api_client.force_authenticate(user=client.user)
    new_mark = Decimal("3.0")
    response = api_client.patch(
        reverse_lazy(
            "api:reviews-detail",
            kwargs={"pk": review.pk},
        ),
        data={
            "mark": new_mark,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert Review.objects.filter(
        id=review.pk,
        mark=new_mark,
    ).exists()


def test_update_review_other_client_by_client(
    client,
    api_client,
) -> None:
    review = ReviewFactory.create()
    api_client.force_authenticate(user=client.user)
    new_mark = Decimal("3.0")
    response = api_client.patch(
        reverse_lazy(
            "api:reviews-detail",
            kwargs={"pk": review.pk},
        ),
        data={
            "mark": new_mark,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_remove_review_by_client(
    client,
    api_client,
) -> None:
    review = ReviewFactory.create(client=client)
    api_client.force_authenticate(user=client.user)
    response = api_client.delete(
        reverse_lazy(
            "api:reviews-detail",
            kwargs={"pk": review.pk},
        ),
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_remove_review_other_client_by_client(
    client,
    api_client,
) -> None:
    review = ReviewFactory.create()
    api_client.force_authenticate(user=client.user)
    response = api_client.delete(
        reverse_lazy(
            "api:reviews-detail",
            kwargs={"pk": review.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_review_by_not_auth(
    api_client,
) -> None:
    review = ReviewFactory.build()
    response = api_client.post(
        reverse_lazy("api:reviews-list"),
        data={
            "review": review.review,
            "mark": review.mark,
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_review_by_not_auth(
    api_client,
) -> None:
    review = ReviewFactory.create()
    new_mark = Decimal("3.0")
    response = api_client.patch(
        reverse_lazy(
            "api:reviews-detail",
            kwargs={"pk": review.pk},
        ),
        data={
            "mark": new_mark,
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_read_review_by_not_auth(
    api_client,
) -> None:
    review = ReviewFactory.create()
    response = api_client.get(
        reverse_lazy(
            "api:reviews-detail",
            kwargs={"pk": review.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_remove_review_by_not_auth(
    api_client,
) -> None:
    review = ReviewFactory.create()
    response = api_client.delete(
        reverse_lazy(
            "api:reviews-detail",
            kwargs={"pk": review.pk},
        ),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
