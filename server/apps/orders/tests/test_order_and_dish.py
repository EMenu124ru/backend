import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.orders.factories import DishFactory, OrderAndDishFactory, OrderFactory
from apps.orders.models import Dish, Order, OrderAndDish
from apps.users.factories import EmployeeFactory
from apps.users.models import Employee

pytestmark = pytest.mark.django_db


def test_create_order_and_dishes_by_cook(
    cook,
    api_client,
) -> None:
    order = OrderFactory.create()
    dish = DishFactory.create()
    order_and_dishes = OrderAndDishFactory.build(order=order, dish=dish)
    api_client.force_authenticate(user=cook.user)
    response = api_client.post(
        reverse_lazy("api:orderAndDishes-list"),
        data={
            "status": order_and_dishes.status,
            "order": order_and_dishes.order.pk,
            "dish": order_and_dishes.dish.pk,
            "comment": order_and_dishes.comment,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert OrderAndDish.objects.filter(
        status=order_and_dishes.status,
        order=order_and_dishes.order,
        dish=order_and_dishes.dish,
        comment=order_and_dishes.comment,
    ).exists()
    assert Dish.objects.get(id=dish.id).orders.exists()
    assert Order.objects.get(id=order.id).dishes.exists()


def test_read_order_and_dishes_by_cook(
    cook,
    api_client,
) -> None:
    order_and_dishes = OrderAndDishFactory.create()
    api_client.force_authenticate(user=cook.user)
    response = api_client.get(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_update_order_and_dishes_by_cook_success(
    cook,
    api_client,
) -> None:
    order_and_dishes = OrderAndDishFactory.create(
        status=OrderAndDish.Statuses.COOKING,
    )
    api_client.force_authenticate(user=cook.user)
    new_status = OrderAndDish.Statuses.DELIVERED
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
        data={
            "status": new_status,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert OrderAndDish.objects.filter(
        status=new_status,
        order=order_and_dishes.order,
        dish=order_and_dishes.dish,
        comment=order_and_dishes.comment,
    ).exists()


def test_update_order_and_dishes_by_chef_success(
    chef,
    api_client,
) -> None:
    order_and_dishes = OrderAndDishFactory.create(
        status=OrderAndDish.Statuses.COOKING,
        employee=None,
    )
    api_client.force_authenticate(user=chef.user)
    new_employee = EmployeeFactory.create(role=Employee.Roles.COOK)
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
        data={
            "employee": new_employee.pk,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert OrderAndDish.objects.filter(
        id=order_and_dishes.pk,
        employee=new_employee.pk,
        order=order_and_dishes.order,
        dish=order_and_dishes.dish,
        comment=order_and_dishes.comment,
    ).exists()


def test_update_order_and_dishes_by_sous_chef_success(
    sous_chef,
    api_client,
) -> None:
    order_and_dishes = OrderAndDishFactory.create(
        status=OrderAndDish.Statuses.COOKING,
        employee=None,
    )
    api_client.force_authenticate(user=sous_chef.user)
    new_employee = EmployeeFactory.create(role=Employee.Roles.COOK)
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
        data={
            "employee": new_employee.pk,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert OrderAndDish.objects.filter(
        id=order_and_dishes.pk,
        employee=new_employee.pk,
        order=order_and_dishes.order,
        dish=order_and_dishes.dish,
        comment=order_and_dishes.comment,
    ).exists()


def test_update_order_and_dishes_by_chef_failed(
    chef,
    api_client,
) -> None:
    order_and_dishes = OrderAndDishFactory.create(
        status=OrderAndDish.Statuses.COOKING,
    )
    api_client.force_authenticate(user=chef.user)
    new_status = OrderAndDish.Statuses.DELIVERED
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
        data={
            "status": new_status,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_order_and_dishes_by_sous_chef_failed(
    sous_chef,
    api_client,
) -> None:
    order_and_dishes = OrderAndDishFactory.create(
        status=OrderAndDish.Statuses.COOKING,
    )
    api_client.force_authenticate(user=sous_chef.user)
    new_status = OrderAndDish.Statuses.DELIVERED
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
        data={
            "status": new_status,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_order_and_dishes_by_cook_failed(
    cook,
    api_client,
) -> None:
    order_and_dishes = OrderAndDishFactory.create()
    api_client.force_authenticate(user=cook.user)
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
        data={
            "comment": "new_comment",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_remove_order_and_dishes_by_cook(
    cook,
    api_client,
) -> None:
    order_and_dishes = OrderAndDishFactory.create()
    api_client.force_authenticate(user=cook.user)
    response = api_client.delete(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert OrderAndDish.objects.filter(id=order_and_dishes.id).exists()


def test_create_order_and_dishes_by_waiter(
    waiter,
    api_client,
) -> None:
    order = OrderFactory.create()
    dish = DishFactory.create()
    order_and_dishes = OrderAndDishFactory.build(order=order, dish=dish)
    api_client.force_authenticate(user=waiter.user)
    response = api_client.post(
        reverse_lazy("api:orderAndDishes-list"),
        data={
            "status": order_and_dishes.status,
            "order": order_and_dishes.order.pk,
            "dish": order_and_dishes.dish.pk,
            "comment": order_and_dishes.comment,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert OrderAndDish.objects.filter(
        status=order_and_dishes.status,
        order=order_and_dishes.order,
        dish=order_and_dishes.dish,
        comment=order_and_dishes.comment,
    ).exists()
    assert Dish.objects.get(id=dish.id).orders.exists()
    assert Order.objects.get(id=order.id).dishes.exists()


def test_read_order_and_dishes_by_waiter(
    waiter,
    api_client,
) -> None:
    order_and_dishes = OrderAndDishFactory.create()
    api_client.force_authenticate(user=waiter.user)
    response = api_client.get(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_update_order_and_dishes_by_waiter_success(
    waiter,
    api_client,
) -> None:
    order_and_dishes = OrderAndDishFactory.create(
        status=OrderAndDish.Statuses.COOKING,
    )
    api_client.force_authenticate(user=waiter.user)
    new_comment = "new_comment"
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
        data={
            "comment": new_comment,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert OrderAndDish.objects.filter(
        comment=new_comment,
        order=order_and_dishes.order,
        dish=order_and_dishes.dish,
        status=order_and_dishes.status,
    ).exists()


def test_update_order_and_dishes_by_waiter_failed(
    waiter,
    api_client,
) -> None:
    order_and_dishes = OrderAndDishFactory.create(
        status=OrderAndDish.Statuses.COOKING,
    )
    api_client.force_authenticate(user=waiter.user)
    new_status = OrderAndDish.Statuses.DELIVERED
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
        data={
            "status": new_status,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_remove_order_and_dishes_by_waiter(
    waiter,
    api_client,
) -> None:
    order_and_dishes = OrderAndDishFactory.create()
    api_client.force_authenticate(user=waiter.user)
    api_client.delete(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
    )
    assert not OrderAndDish.objects.filter(id=order_and_dishes.id).exists()


def test_create_order_and_dishes_by_client(
    client,
    api_client,
) -> None:
    order = OrderFactory.create()
    dish = DishFactory.create()
    order_and_dishes = OrderAndDishFactory.build(order=order, dish=dish)
    api_client.force_authenticate(user=client.user)
    response = api_client.post(
        reverse_lazy("api:orderAndDishes-list"),
        data={
            "status": order_and_dishes.status,
            "order": order_and_dishes.order.pk,
            "dish": order_and_dishes.dish.pk,
            "comment": order_and_dishes.comment,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_read_order_and_dishes_by_client(
    client,
    api_client,
) -> None:
    order_and_dishes = OrderAndDishFactory.create()
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_order_and_dishes_by_client(
    client,
    api_client,
) -> None:
    order_and_dishes = OrderAndDishFactory.create(
        status=OrderAndDish.Statuses.COOKING,
    )
    api_client.force_authenticate(user=client.user)
    new_status = OrderAndDish.Statuses.DELIVERED
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
        data={
            "status": new_status,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_remove_order_and_dishes_by_client(
    client,
    api_client,
) -> None:
    order_and_dishes = OrderAndDishFactory.create()
    api_client.force_authenticate(user=client.user)
    response = api_client.delete(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_order_and_dishes_by_not_auth(
    api_client,
) -> None:
    order = OrderFactory.create()
    dish = DishFactory.create()
    order_and_dishes = OrderAndDishFactory.build(order=order, dish=dish)
    response = api_client.post(
        reverse_lazy("api:orderAndDishes-list"),
        data={
            "status": order_and_dishes.status,
            "order": order_and_dishes.order.pk,
            "dish": order_and_dishes.dish.pk,
            "comment": order_and_dishes.comment,
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_read_order_and_dishes_by_not_auth(
    api_client,
) -> None:
    order_and_dishes = OrderAndDishFactory.create()
    response = api_client.get(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_order_and_dishes_by_not_auth(
    api_client,
) -> None:
    order_and_dishes = OrderAndDishFactory.create(
        status=OrderAndDish.Statuses.COOKING,
    )
    new_status = OrderAndDish.Statuses.DELIVERED
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
        data={
            "status": new_status,
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_order_and_dishes_by_not_auth(
    api_client,
) -> None:
    order_and_dishes = OrderAndDishFactory.create()
    response = api_client.delete(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
