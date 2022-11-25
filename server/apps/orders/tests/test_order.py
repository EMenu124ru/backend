import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.orders.factories import DishFactory, OrderAndDishesFactory, OrderFactory
from apps.orders.models import Order, OrderAndDishes
from apps.users.factories import ClientFactory, EmployeeFactory

pytestmark = pytest.mark.django_db

DISHES_COUNT = 6
ORDERS_COUNT = 3


def test_create_order_by_waiter(
    waiter,
    api_client,
) -> None:
    client = ClientFactory.create()
    order = OrderFactory.build()
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    api_client.force_authenticate(user=waiter.user)
    sum_dishes_prices = sum([dish.price for dish in dishes])
    response = api_client.post(
        reverse_lazy("api:orders-list"),
        data={
            "status": order.status,
            "price": sum_dishes_prices,
            "comment": order.comment,
            "client": client.pk,
            "place_number": order.place_number,
            "dishes": [dish.id for dish in dishes],
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Order.objects.filter(
        status=order.status,
        price=sum_dishes_prices,
        comment=order.comment,
        client=client.pk,
        employee=waiter.pk,
        place_number=order.place_number,
    ).exists()


def test_update_order_by_waiter(
    waiter,
    api_client,
) -> None:
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    order = OrderFactory.create(
        employee=waiter,
        price=sum([dish.price for dish in dishes]),
    )
    api_client.force_authenticate(user=waiter.user)
    new_place_number = 3
    response = api_client.patch(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
        data={
            "place_number": new_place_number,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert Order.objects.filter(
        place_number=new_place_number,
    ).exists()


def test_update_order_by_waiter_change_dishes(
    waiter,
    api_client,
) -> None:
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    order = OrderFactory.create(
        employee=waiter,
        price=sum([dish.price for dish in dishes]),
    )
    for dish in dishes:
        OrderAndDishesFactory.create(dish=dish, order=order)
    delete, existed = dishes[:DISHES_COUNT // 2], dishes[DISHES_COUNT // 2:]
    new_dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    dishes = existed + new_dishes
    api_client.force_authenticate(user=waiter.user)
    response = api_client.patch(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
        data={
            "dishes": [dish.id for dish in dishes],
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert OrderAndDishes.objects.filter(
        order=order,
        dish__id__in=[dish.id for dish in dishes],
    ).exists()
    assert not OrderAndDishes.objects.filter(
        order=order,
        dish__id__in=[dish.id for dish in delete],
    ).exists()


def test_update_order_by_cook_failed(
    cook,
    waiter,
    api_client,
) -> None:
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    order = OrderFactory.create(
        employee=waiter,
        price=sum([dish.price for dish in dishes]),
    )
    api_client.force_authenticate(user=cook.user)
    new_place_number = order.place_number + 3
    response = api_client.patch(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
        data={
            "place_number": new_place_number,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_order_by_cook_success(
    cook,
    waiter,
    api_client,
) -> None:
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    order = OrderFactory.create(
        employee=waiter,
        price=sum([dish.price for dish in dishes]),
    )
    api_client.force_authenticate(user=cook.user)
    new_comment = "New some comment"
    new_status = Order.Statuses.COOKING
    response = api_client.patch(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
        data={
            "comment": new_comment,
            "status": new_status,
            "place_number": order.place_number,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert Order.objects.filter(
        id=order.pk,
        comment=new_comment,
        status=new_status,
    ).exists()


def test_read_orders_by_waiter(
    waiter,
    api_client,
) -> None:
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    OrderFactory.create_batch(
        employee=waiter,
        price=sum([dish.price for dish in dishes]),
        size=ORDERS_COUNT,
    )
    api_client.force_authenticate(user=waiter.user)
    response = api_client.get(
        reverse_lazy(
            "api:orders-list",
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_order_by_waiter(
    waiter,
    api_client,
) -> None:
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    sum_dishes_prices = sum([dish.price for dish in dishes])
    order = OrderFactory.create(
        employee=waiter,
        price=sum_dishes_prices,
    )
    api_client.force_authenticate(user=waiter.user)
    response = api_client.get(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_remove_order_by_waiter(
    waiter,
    api_client,
) -> None:
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    order = OrderFactory.create(
        employee=waiter,
        price=sum([dish.price for dish in dishes]),
    )
    api_client.force_authenticate(user=waiter.user)
    api_client.delete(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
    )
    assert order not in Order.objects.all()


def test_create_order_by_client(
    client,
    api_client,
) -> None:
    order = OrderFactory.build()
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    api_client.force_authenticate(user=client.user)
    sum_dishes_prices = sum([dish.price for dish in dishes])
    response = api_client.post(
        reverse_lazy("api:orders-list"),
        data={
            "status": order.status,
            "price": sum_dishes_prices,
            "comment": order.comment,
            "client": client.pk,
            "place_number": order.place_number,
            "dishes": [dish.id for dish in dishes],
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_order_by_client_failed(
    client,
    api_client,
) -> None:
    dishes = OrderAndDishesFactory.create_batch(
        size=DISHES_COUNT,
    )
    order = OrderFactory.create(
        client=client,
        price=sum([dish.dish.price for dish in dishes]),
    )
    order.dishes.set(dishes)
    api_client.force_authenticate(user=client.user)
    new_place_number = order.place_number + 3
    response = api_client.patch(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
        data={
            "place_number": new_place_number,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_order_by_client_success(
    client,
    api_client,
) -> None:
    dishes = OrderAndDishesFactory.create_batch(
        size=DISHES_COUNT,
    )
    order = OrderFactory.create(
        client=client,
        price=sum([dish.dish.price for dish in dishes]),
    )
    order.dishes.set(dishes)
    api_client.force_authenticate(user=client.user)
    new_dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    response = api_client.patch(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
        data={
            "dishes": [dish.id for dish in new_dishes],
            "place_number": order.place_number,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert Order.objects.filter(
        id=order.pk,
        place_number=order.place_number,
    )
    assert OrderAndDishes.objects.filter(
        order=order.pk,
        dish__id__in=[dish.id for dish in new_dishes],
    ).exists()


def test_read_orders_by_client(
    client,
    api_client,
) -> None:
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    OrderFactory.create_batch(
        price=sum([dish.price for dish in dishes]),
        size=ORDERS_COUNT,
    )
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
        reverse_lazy("api:orders-list"),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_read_order_by_client_failed(
    client,
    api_client,
) -> None:
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    order = OrderFactory.create(
        price=sum([dish.price for dish in dishes]),
    )
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_read_order_by_client_success(
    client,
    api_client,
) -> None:
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    order = OrderFactory.create(
        client=client,
        price=sum([dish.price for dish in dishes]),
    )
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_remove_order_by_client(
    client,
    api_client,
) -> None:
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    order = OrderFactory.create(
        client=client,
        price=sum([dish.price for dish in dishes]),
    )
    api_client.force_authenticate(user=client.user)
    response = api_client.delete(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_order_by_not_auth(
    api_client,
) -> None:
    client = ClientFactory.create()
    employee = EmployeeFactory.create()
    order = OrderFactory.build()
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    sum_dishes_prices = sum([dish.price for dish in dishes])
    response = api_client.post(
        reverse_lazy("api:orders-list"),
        data={
            "status": order.status,
            "price": sum_dishes_prices,
            "comment": order.comment,
            "client": client.pk,
            "employee": employee.pk,
            "place_number": order.place_number,
            "dishes": [dish.id for dish in dishes],
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_order_by_not_auth(
    api_client,
) -> None:
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    order = OrderFactory.create(
        price=sum([dish.price for dish in dishes]),
    )
    new_comment = "Sample comment"
    response = api_client.patch(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
        data={
            "comment": new_comment,
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_read_orders_by_not_auth(
    api_client,
) -> None:
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    OrderFactory.create_batch(
        price=sum([dish.price for dish in dishes]),
        size=ORDERS_COUNT,
    )
    response = api_client.get(
        reverse_lazy(
            "api:orders-list",
        ),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_read_order_by_not_auth(
    api_client,
) -> None:
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    order = OrderFactory.create(
        price=sum([dish.price for dish in dishes]),
    )
    response = api_client.get(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_remove_order_by_not_auth(
    api_client,
) -> None:
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    order = OrderFactory.create(
        price=sum([dish.price for dish in dishes]),
    )
    response = api_client.delete(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
