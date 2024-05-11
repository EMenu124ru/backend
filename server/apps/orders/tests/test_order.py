import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.orders.factories import (
    DishFactory,
    OrderFactory,
    ReservationFactory,
)
from apps.orders.models import Order, Reservation
from apps.restaurants.factories import PlaceFactory
from apps.users.factories import ClientFactory, EmployeeFactory
from apps.users.models import Employee

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
    place = PlaceFactory.create(restaurant=waiter.restaurant)
    api_client.force_authenticate(user=waiter.user)
    sum_dishes_prices = sum([dish.price for dish in dishes])
    place_pk = place.pk
    response = api_client.post(
        reverse_lazy("api:orders-list"),
        data={
            "price": sum_dishes_prices,
            "comment": order.comment,
            "client": client.pk,
            "dishes": [
                {"dish": dish.id} for dish in dishes
            ],
            "place": place_pk,
        },
        format='json',
    )
    assert response.status_code == status.HTTP_201_CREATED
    query = Order.objects.filter(
        status=Order.Statuses.WAITING_FOR_COOKING,
        price=sum_dishes_prices,
        comment=order.comment,
        client=client.pk,
        employee=waiter.pk,
    )
    assert query.exists()
    order = query.first()
    assert order.reservation is not None
    assert order.reservation.place.pk == place_pk


def test_create_order_by_waiter_without_client(
    waiter,
    api_client,
) -> None:
    order = OrderFactory.build()
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    place = PlaceFactory.create(restaurant=waiter.restaurant)
    api_client.force_authenticate(user=waiter.user)
    sum_dishes_prices = sum([dish.price for dish in dishes])
    place_pk = place.pk
    response = api_client.post(
        reverse_lazy("api:orders-list"),
        data={
            "price": sum_dishes_prices,
            "comment": order.comment,
            "dishes": [
                {"dish": dish.id} for dish in dishes
            ],
            "place": place_pk,
        },
        format='json',
    )
    assert response.status_code == status.HTTP_201_CREATED
    query = Order.objects.filter(
        status=Order.Statuses.WAITING_FOR_COOKING,
        price=sum_dishes_prices,
        comment=order.comment,
        client=None,
        employee=waiter.pk,
    )
    assert query.exists()
    order = query.first()
    assert order.reservation is not None
    assert order.reservation.place.pk == place_pk


def test_create_order_by_waiter_with_reservation(
    waiter,
    api_client,
) -> None:
    client = ClientFactory.create()
    reservation = ReservationFactory.create(
        status=Reservation.Statuses.OPENED,
        restaurant=waiter.restaurant,
    )
    order = OrderFactory.build(
        employee=waiter,
        reservation=reservation,
    )
    dishes = DishFactory.create_batch(size=DISHES_COUNT)
    api_client.force_authenticate(user=waiter.user)
    sum_dishes_prices = sum([dish.price for dish in dishes])
    response = api_client.post(
        reverse_lazy("api:orders-list"),
        data={
            "status": order.status,
            "price": sum_dishes_prices,
            "comment": order.comment,
            "client": client.pk,
            "dishes": [
                {"dish": dish.id} for dish in dishes
            ],
            "reservation": order.reservation.pk,
        },
        format='json',
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Order.objects.filter(
        id=response.data["id"],
        status=Order.Statuses.DELAYED,
        price=sum_dishes_prices,
        comment=order.comment,
        client=client.pk,
        employee=waiter.pk,
        reservation=order.reservation.pk
    ).exists()


def test_update_order_by_cook(
    cook,
    api_client,
) -> None:
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    waiter = EmployeeFactory.create(
        restaurant=cook.restaurant,
        role=Employee.Roles.WAITER,
    )
    order = OrderFactory.create(
        employee=waiter,
        price=sum([dish.price for dish in dishes]),
        status=Order.Statuses.WAITING_FOR_COOKING,
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
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_order_by_waiter_success(
    waiter,
    api_client,
) -> None:
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    order = OrderFactory.create(
        employee=waiter,
        price=sum([dish.price for dish in dishes]),
        status=Order.Statuses.WAITING_FOR_COOKING,
    )
    api_client.force_authenticate(user=waiter.user)
    new_comment = "New some comment"
    response = api_client.patch(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
        data={
            "comment": new_comment,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert Order.objects.filter(
        id=order.pk,
        comment=new_comment,
    ).exists()


def test_update_order_by_waiter_failed(
    waiter,
    api_client,
) -> None:
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    order = OrderFactory.create(
        employee=waiter,
        price=sum([dish.price for dish in dishes]),
        status=Order.Statuses.WAITING_FOR_COOKING,
    )
    api_client.force_authenticate(user=waiter.user)
    new_employee = EmployeeFactory.create()
    response = api_client.patch(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
        data={
            "employee": new_employee.pk,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Order.objects.filter(
        id=order.pk,
        employee=order.employee,
    ).exists()


def test_update_order_by_waiter_status_failed(
    waiter,
    api_client,
) -> None:
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    order = OrderFactory.create(
        employee=waiter,
        price=sum([dish.price for dish in dishes]),
        status=Order.Statuses.WAITING_FOR_COOKING,
    )
    api_client.force_authenticate(user=waiter.user)
    response = api_client.patch(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
        data={
            "status": Order.Statuses.COOKING,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Order.objects.filter(
        id=order.pk,
        status=order.status,
    ).exists()


def test_update_order_by_waiter_status_success(
    waiter,
    api_client,
) -> None:
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    order = OrderFactory.create(
        employee=waiter,
        price=sum([dish.price for dish in dishes]),
        status=Order.Statuses.WAITING_FOR_COOKING,
    )
    api_client.force_authenticate(user=waiter.user)

    new_status = Order.Statuses.PAID
    response = api_client.patch(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
        data={
            "status": new_status,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert Order.objects.filter(
        id=order.pk,
        status=new_status,
    ).exists()

    new_status = Order.Statuses.FINISHED
    response = api_client.patch(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
        data={
            "status": new_status,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert Order.objects.filter(
        id=order.pk,
        status=new_status,
    ).exists()


def test_update_order_by_waiter_status_cancel(
    waiter,
    api_client,
) -> None:
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    order = OrderFactory.create(
        employee=waiter,
        price=sum([dish.price for dish in dishes]),
        status=Order.Statuses.WAITING_FOR_COOKING,
    )
    api_client.force_authenticate(user=waiter.user)

    new_status = Order.Statuses.CANCELED
    response = api_client.patch(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
        data={
            "status": new_status,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert Order.objects.filter(
        id=order.pk,
        status=new_status,
    ).exists()

    new_status = Order.Statuses.FINISHED
    response = api_client.patch(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
        data={
            "status": new_status,
        },
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Order.objects.filter(
        id=order.pk,
        status=Order.Statuses.CANCELED,
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
        status=Order.Statuses.WAITING_FOR_COOKING,
    )
    api_client.force_authenticate(user=waiter.user)
    response = api_client.get(
        reverse_lazy(
            "api:orders-list",
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_orders_by_manager(
    manager,
    waiter,
    api_client,
) -> None:
    waiter.restaurant = manager.restaurant
    waiter.save()
    OrderFactory.create_batch(
        employee=waiter,
        size=ORDERS_COUNT,
        status=Order.Statuses.WAITING_FOR_COOKING,
    )
    api_client.force_authenticate(user=manager.user)
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
        status=Order.Statuses.WAITING_FOR_COOKING,
    )
    api_client.force_authenticate(user=waiter.user)
    response = api_client.get(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_order_by_waiter_from_other_restaurant(
    waiter,
    api_client,
) -> None:
    dishes = DishFactory.create_batch(
        size=DISHES_COUNT,
    )
    sum_dishes_prices = sum([dish.price for dish in dishes])
    order = OrderFactory.create(
        price=sum_dishes_prices,
        status=Order.Statuses.WAITING_FOR_COOKING,
    )
    api_client.force_authenticate(user=waiter.user)
    response = api_client.get(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_order_by_client(
    client,
    api_client,
) -> None:
    order = OrderFactory.build(status=Order.Statuses.WAITING_FOR_COOKING)
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
            "dishes": [dish.id for dish in dishes],
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


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
        status=Order.Statuses.WAITING_FOR_COOKING,
    )
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
        reverse_lazy("api:orders-list"),
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
        status=Order.Statuses.WAITING_FOR_COOKING,
    )
    api_client.force_authenticate(user=client.user)
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
        status=Order.Statuses.WAITING_FOR_COOKING,
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
        status=Order.Statuses.WAITING_FOR_COOKING,
    )
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
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
    order = OrderFactory.build(status=Order.Statuses.WAITING_FOR_COOKING)
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
        status=Order.Statuses.WAITING_FOR_COOKING,
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
        status=Order.Statuses.WAITING_FOR_COOKING,
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
        status=Order.Statuses.WAITING_FOR_COOKING,
    )
    response = api_client.get(
        reverse_lazy(
            "api:orders-detail",
            kwargs={"pk": order.pk},
        ),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
