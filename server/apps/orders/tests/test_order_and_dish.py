import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.orders.factories import (
    DishFactory,
    OrderAndDishFactory,
    OrderFactory,
)
from apps.orders.models import (
    Dish,
    Order,
    OrderAndDish,
)
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
            "count": order_and_dishes.count,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_order_and_dishes_by_cook_success(
    cook,
    api_client,
) -> None:
    waiter = EmployeeFactory.create(
        restaurant=cook.restaurant,
        role=Employee.Roles.WAITER,
    )
    order = OrderFactory.create(employee=waiter)
    order_and_dishes = OrderAndDishFactory.create(
        order=order,
        status=OrderAndDish.Statuses.COOKING,
        employee=cook,
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
        count=order_and_dishes.count,
    ).exists()


def test_update_order_and_dishes_by_chef_success(
    chef,
    api_client,
) -> None:
    waiter = EmployeeFactory.create(
        restaurant=chef.restaurant,
        role=Employee.Roles.WAITER,
    )
    order = OrderFactory.create(employee=waiter)
    order_and_dishes = OrderAndDishFactory.create(
        order=order,
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
        count=order_and_dishes.count,
    ).exists()


def test_update_order_and_dishes_by_sous_chef_success(
    sous_chef,
    api_client,
) -> None:
    waiter = EmployeeFactory.create(
        restaurant=sous_chef.restaurant,
        role=Employee.Roles.WAITER,
    )
    order = OrderFactory.create(employee=waiter)
    order_and_dishes = OrderAndDishFactory.create(
        order=order,
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
        count=order_and_dishes.count,
    ).exists()


def test_update_order_and_dishes_by_chef_failed_field(
    chef,
    api_client,
) -> None:
    waiter = EmployeeFactory.create(
        restaurant=chef.restaurant,
        role=Employee.Roles.WAITER,
    )
    order = OrderFactory.create(employee=waiter)
    order_and_dishes = OrderAndDishFactory.create(
        order=order,
        status=OrderAndDish.Statuses.COOKING,
    )
    api_client.force_authenticate(user=chef.user)
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
        data={
            "order": OrderFactory.create().pk,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_order_and_dishes_by_sous_chef_failed_field(
    sous_chef,
    api_client,
) -> None:
    waiter = EmployeeFactory.create(
        restaurant=sous_chef.restaurant,
        role=Employee.Roles.WAITER,
    )
    order = OrderFactory.create(employee=waiter)
    order_and_dishes = OrderAndDishFactory.create(
        order=order,
        status=OrderAndDish.Statuses.COOKING,
    )
    api_client.force_authenticate(user=sous_chef.user)
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
        data={
            "order": OrderFactory.create().pk,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_order_and_dishes_by_cook_failed_field(
    cook,
    chef,
    api_client,
) -> None:
    waiter = EmployeeFactory.create(
        restaurant=cook.restaurant,
        role=Employee.Roles.WAITER,
    )
    order = OrderFactory.create(
        employee=waiter,
        status=Order.Statuses.WAITING_FOR_COOKING,
    )
    order_and_dishes = OrderAndDishFactory.create(
        order=order,
        status=OrderAndDish.Statuses.WAITING_FOR_COOKING,
        employee=None,
    )
    api_client.force_authenticate(user=cook.user)
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
        data={
            "employee": chef.pk,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_order_and_dishes_by_chef_failed(
    chef,
    api_client,
) -> None:
    order_and_dishes = OrderAndDishFactory.create(
        status=OrderAndDish.Statuses.COOKING,
    )
    api_client.force_authenticate(user=chef.user)
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
        data={
            "order": OrderFactory.create().pk,
        },
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_order_and_dishes_by_chef_failed_current_restaurant(
    chef,
    waiter,
    api_client,
) -> None:
    waiter.restaurant = chef.restaurant
    waiter.save()
    order = OrderFactory.create(employee=waiter)
    order_and_dishes = OrderAndDishFactory.create(
        status=OrderAndDish.Statuses.COOKING,
        order=order,
    )
    api_client.force_authenticate(user=chef.user)
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
        data={
            "order": OrderFactory.create().pk,
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
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
        data={
            "order": OrderFactory.create().pk,
        },
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_order_and_dishes_by_sous_chef_failed_current_restaurant(
    sous_chef,
    api_client,
) -> None:
    waiter = EmployeeFactory.create(
        restaurant=sous_chef.restaurant,
        role=Employee.Roles.WAITER,
    )
    order = OrderFactory.create(employee=waiter)
    order_and_dishes = OrderAndDishFactory.create(
        status=OrderAndDish.Statuses.COOKING,
        order=order,
    )
    api_client.force_authenticate(user=sous_chef.user)
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
        data={
            "order": OrderFactory.create().pk,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_order_and_dishes_by_cook_failed(
    cook,
    chef,
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
            "employee": chef.pk,
        },
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_order_and_dishes_by_cook_failed_current_restaurant(
    cook,
    chef,
    api_client,
) -> None:
    waiter = EmployeeFactory.create(
        restaurant=cook.restaurant,
        role=Employee.Roles.WAITER,
    )
    order = OrderFactory.create(
        employee=waiter,
        status=Order.Statuses.WAITING_FOR_COOKING,
    )
    order_and_dishes = OrderAndDishFactory.create(
        order=order,
        status=OrderAndDish.Statuses.WAITING_FOR_COOKING,
    )
    api_client.force_authenticate(user=cook.user)
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
        data={
            "employee": chef.pk,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_order_and_dishes_by_waiter(
    waiter,
    api_client,
) -> None:
    order = OrderFactory.create(
        status=Order.Statuses.WAITING_FOR_COOKING,
    )
    dish = DishFactory.create()
    order_and_dishes = OrderAndDishFactory.build(
        order=order,
        dish=dish,
        status=OrderAndDish.Statuses.WAITING_FOR_COOKING,
        employee=None,
    )
    api_client.force_authenticate(user=waiter.user)
    response = api_client.post(
        reverse_lazy("api:orderAndDishes-list"),
        data={
            "status": order_and_dishes.status,
            "order": order_and_dishes.order.pk,
            "dish": order_and_dishes.dish.pk,
            "count": order_and_dishes.count,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert OrderAndDish.objects.filter(
        status=order_and_dishes.status,
        order=order_and_dishes.order,
        dish=order_and_dishes.dish,
        count=order_and_dishes.count,
    ).exists()
    assert Dish.objects.get(id=dish.id).orders.exists()
    assert Order.objects.get(id=order.id).dishes.exists()


def test_create_more_one_order_and_dishes_by_waiter(
    waiter,
    api_client,
) -> None:
    order = OrderFactory.create(
        status=Order.Statuses.WAITING_FOR_COOKING,
        employee=waiter,
    )
    dish = DishFactory.create()
    order_and_dishes = OrderAndDishFactory.build(
        order=order,
        dish=dish,
        employee=None,
        status=OrderAndDish.Statuses.WAITING_FOR_COOKING,
    )
    api_client.force_authenticate(user=waiter.user)
    order_body = {
        "status": order_and_dishes.status,
        "order": order_and_dishes.order.pk,
        "dish": order_and_dishes.dish.pk,
        "count": order_and_dishes.count,
        "comment": "some comment",
    }
    response = api_client.post(
        reverse_lazy("api:orderAndDishes-list"),
        data=order_body,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert OrderAndDish.objects.filter(**order_body).exists()
    assert Dish.objects.get(id=dish.id).orders.exists()
    assert Order.objects.get(id=order.id).dishes.count() == 1

    order_body["count"] = 1
    order_body["comment"] = "some comment 123"
    response = api_client.post(
        reverse_lazy("api:orderAndDishes-list"),
        data=order_body,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert OrderAndDish.objects.filter(**order_body).exists()
    assert Order.objects.get(id=order.id).dishes.count() == 2


def test_create_order_and_dishes_by_waiter_zero_count(
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
            "count": 0,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not OrderAndDish.objects.filter(
        status=order_and_dishes.status,
        order=order_and_dishes.order,
        dish=order_and_dishes.dish,
        count=0,
    ).exists()


def test_update_order_and_dishes_by_waiter_success(
    waiter,
    api_client,
) -> None:
    order = OrderFactory.create(employee=waiter)
    order_and_dishes = OrderAndDishFactory.create(
        order=order,
        status=OrderAndDish.Statuses.COOKING,
    )
    api_client.force_authenticate(user=waiter.user)
    new_count = order_and_dishes.count + 1
    new_status = OrderAndDish.Statuses.DELIVERED
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
        data={
            "count": new_count,
            "status": new_status,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert OrderAndDish.objects.filter(
        count=new_count,
        order=order_and_dishes.order,
        dish=order_and_dishes.dish,
        status=new_status,
    ).exists()


def test_update_order_and_dishes_by_waiter_failed_zero_count(
    waiter,
    api_client,
) -> None:
    order = OrderFactory.create(employee=waiter)
    order_and_dishes = OrderAndDishFactory.create(
        order=order,
        count=5,
        status=OrderAndDish.Statuses.COOKING,
    )
    api_client.force_authenticate(user=waiter.user)
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
        data={
            "count": 0,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not OrderAndDish.objects.filter(
        count=0,
        order=order_and_dishes.order,
        dish=order_and_dishes.dish,
        status=order_and_dishes.status,
    ).exists()


def test_update_order_and_dishes_by_waiter_failed(
    waiter,
    cook,
    api_client,
) -> None:
    order = OrderFactory.create(employee=waiter)
    order_and_dishes = OrderAndDishFactory.create(
        order=order,
        status=OrderAndDish.Statuses.COOKING,
    )
    api_client.force_authenticate(user=waiter.user)
    response = api_client.patch(
        reverse_lazy(
            "api:orderAndDishes-detail",
            kwargs={"pk": order_and_dishes.pk},
        ),
        data={
            "employee": cook.pk,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


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
            "count": order_and_dishes.count,
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
            "count": order_and_dishes.count,
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
