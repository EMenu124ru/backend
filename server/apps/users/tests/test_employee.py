import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.restaurants.factories import RestaurantFactory
from apps.users.factories import EmployeeFactory
from apps.users.models import Employee

pytestmark = pytest.mark.django_db


def test_get_me_employee(
    api_client,
    waiter,
) -> None:
    api_client.force_authenticate(user=waiter.user)
    response = api_client.get(reverse_lazy("api:staff-detail"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == waiter.id


def test_get_me_employee_not_auth(
    api_client,
) -> None:
    api_client.force_authenticate()
    response = api_client.get(reverse_lazy("api:staff-detail"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_kitchen_employees_chef(chef, api_client):
    api_client.force_authenticate(user=chef.user)
    response = api_client.get(reverse_lazy("api:staff-kitchen"))
    assert response.status_code == status.HTTP_200_OK


def test_get_kitchen_employees_manager(manager, api_client):
    api_client.force_authenticate(user=manager.user)
    response = api_client.get(reverse_lazy("api:staff-kitchen"))
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_kitchen_employees_client(client, api_client):
    api_client.force_authenticate(user=client.user)
    response = api_client.get(reverse_lazy("api:staff-kitchen"))
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_kitchen_employees_not_auth(api_client):
    response = api_client.get(reverse_lazy("api:staff-kitchen"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_employees_by_roles_chef(chef, api_client):
    api_client.force_authenticate(user=chef.user)
    response = api_client.get(reverse_lazy("api:staff-list"))
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_employees_by_roles_manager(manager, api_client):
    api_client.force_authenticate(user=manager.user)
    response = api_client.get(reverse_lazy("api:staff-list"))
    assert response.status_code == status.HTTP_200_OK


def test_get_employees_by_roles_client(client, api_client):
    api_client.force_authenticate(user=client.user)
    response = api_client.get(reverse_lazy("api:staff-list"))
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_employees_by_roles_not_auth(api_client):
    response = api_client.get(reverse_lazy("api:staff-list"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_employee_by_manager_success(
    api_client,
    manager,
):
    waiter = EmployeeFactory.create(
        restaurant=manager.restaurant,
        role=Employee.Roles.WAITER,
    )
    api_client.force_authenticate(user=manager.user)
    new_education = "СФУ ИКИТ"
    response = api_client.patch(
        reverse_lazy("api:staff-update", kwargs={"pk": waiter.pk}),
        data={
            "education": new_education,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert Employee.objects.filter(pk=waiter.pk, education=new_education).exists()


def test_update_employee_by_manager_failed(
    api_client,
    manager,
):
    restaurant = RestaurantFactory.create()
    waiter = EmployeeFactory.create(
        restaurant=manager.restaurant,
        role=Employee.Roles.WAITER,
    )
    api_client.force_authenticate(user=manager.user)
    response = api_client.patch(
        reverse_lazy("api:staff-update", kwargs={"pk": waiter.pk}),
        data={
            "restaurant": restaurant.pk,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not Employee.objects.filter(pk=waiter.pk, restaurant=restaurant.pk).exists()

    new_email = "newemail@mail.ru"
    response = api_client.patch(
        reverse_lazy("api:staff-update", kwargs={"pk": waiter.pk}),
        data={
            "email": new_email,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert Employee.objects.filter(pk=waiter.pk, user__email=new_email).exists()


def test_get_schedule_employee(
    api_client,
    waiter,
) -> None:
    api_client.force_authenticate(user=waiter.user)
    response = api_client.get(
        reverse_lazy("api:staff-schedule", kwargs={"pk": waiter.pk})
    )
    assert response.status_code == status.HTTP_200_OK


def test_get_schedule_employee_other_restaurant(
    api_client,
    waiter,
) -> None:
    staff = EmployeeFactory.create()
    while staff.restaurant.id == waiter.restaurant.id:
        staff = EmployeeFactory.create()
    api_client.force_authenticate(user=staff.user)
    response = api_client.get(
        reverse_lazy("api:staff-schedule", kwargs={"pk": waiter.pk})
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_schedule_employee_not_auth(
    api_client,
    waiter,
) -> None:
    api_client.force_authenticate()
    response = api_client.get(
        reverse_lazy("api:staff-schedule", kwargs={"pk": waiter.pk})
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
