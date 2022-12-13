import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.orders.factories import OrderFactory, DishFactory
from apps.users.factories import ClientFactory, EmployeeFactory
from apps.orders.models import Order

pytestmark = pytest.mark.django_db

DISHES_COUNT = 3


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
    client = ClientFactory.create()
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    sum_dishes_prices = sum([dish.price for dish in dishes])
    order = OrderFactory.create(
        client=client,
        employee=waiter,
        price=sum_dishes_prices,
    )
    api_client.force_authenticate(user=waiter.user)
    new_comment = "Sample comment"
    response = api_client.put(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
        data={
            "status": order.status,
            "price": sum_dishes_prices,
            "client": client.pk,
            "place_number": order.place_number,
            "dishes": [dish.id for dish in dishes],
            "comment": new_comment,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert Order.objects.filter(
        comment=new_comment,
        status=order.status,
        price=sum_dishes_prices,
    ).exists()


def test_read_order_by_waiter(
    waiter,
    api_client,
) -> None:
    client = ClientFactory.create()
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    sum_dishes_prices = sum([dish.price for dish in dishes])
    order = OrderFactory.create(
        client=client,
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
    client = ClientFactory.create()
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    sum_dishes_prices = sum([dish.price for dish in dishes])
    order = OrderFactory.create(
        client=client,
        employee=waiter,
        price=sum_dishes_prices,
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
    employee = EmployeeFactory.create()
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


def test_update_order_by_client(
    client,
    api_client,
) -> None:
    employee = EmployeeFactory.create()
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    sum_dishes_prices = sum([dish.price for dish in dishes])
    order = OrderFactory.create(
        client=client,
        employee=employee,
        price=sum_dishes_prices,
    )
    api_client.force_authenticate(user=client.user)
    new_comment = "Sample comment"
    response = api_client.put(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
        data={
            "status": order.status,
            "price": sum_dishes_prices,
            "client": client.pk,
            "place_number": order.place_number,
            "dishes": [dish.id for dish in dishes],
            "comment": order.comment,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_read_order_by_client(
    client,
    api_client,
) -> None:
    employee = EmployeeFactory.create()
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    sum_dishes_prices = sum([dish.price for dish in dishes])
    order = OrderFactory.create(
        client=client,
        employee=employee,
        price=sum_dishes_prices,
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
    employee = EmployeeFactory.create()
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    sum_dishes_prices = sum([dish.price for dish in dishes])
    order = OrderFactory.create(
        client=client,
        employee=employee,
        price=sum_dishes_prices,
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
    client = ClientFactory.create()
    employee = EmployeeFactory.create()
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    sum_dishes_prices = sum([dish.price for dish in dishes])
    order = OrderFactory.create(
        client=client,
        employee=employee,
        price=sum_dishes_prices,
    )
    new_comment = "Sample comment"
    response = api_client.put(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
        data={
            "status": order.status,
            "price": sum_dishes_prices,
            "client": client.pk,
            "place_number": order.place_number,
            "dishes": [dish.id for dish in dishes],
            "comment": new_comment,
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_read_order_by_not_auth(
    api_client,
) -> None:
    client = ClientFactory.create()
    employee = EmployeeFactory.create()
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    sum_dishes_prices = sum([dish.price for dish in dishes])
    order = OrderFactory.create(
        client=client,
        employee=employee,
        price=sum_dishes_prices,
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
    client = ClientFactory.create()
    employee = EmployeeFactory.create()
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    sum_dishes_prices = sum([dish.price for dish in dishes])
    order = OrderFactory.create(
        client=client,
        employee=employee,
        price=sum_dishes_prices,
    )
    response = api_client.delete(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_remove_order_by_hostess(
    hostess,
    api_client,
) -> None:
    client = ClientFactory.create()
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    waiter = ClientFactory.create()
    sum_dishes_prices = sum([dish.price for dish in dishes])
    order = OrderFactory.create(
        client=client,
        employee=waiter,
        price=sum_dishes_prices,
    )
    api_client.force_authenticate(user=hostess.user)
    api_client.delete(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
    )
    assert order not in Order.objects.all()
