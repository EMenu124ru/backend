import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.users.factories import EmployeeFactory, ScheduleFactory
from apps.users.models import Employee, Schedule

pytestmark = pytest.mark.django_db


def test_update_schedule_manager(
    api_client,
    manager,
):
    waiter = EmployeeFactory.create(
        restaurant=manager.restaurant,
        role=Employee.Roles.WAITER,
    )
    schedule = ScheduleFactory.create(employee=waiter)
    api_client.force_authenticate(user=manager.user)
    new_approve = not schedule.is_approve
    response = api_client.patch(
        reverse_lazy(
            "api:employeeSchedule-detail",
            kwargs={"pk": schedule.pk},
        ),
        data={
            "is_approve": new_approve,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert Schedule.objects.filter(
        pk=schedule.pk,
        is_approve=new_approve,
    ).exists()


def test_update_schedule_waiter(
    api_client,
    waiter,
):
    schedule = ScheduleFactory.create(employee=waiter)
    api_client.force_authenticate(user=waiter.user)
    new_approve = not schedule.is_approve
    response = api_client.patch(
        reverse_lazy(
            "api:employeeSchedule-detail",
            kwargs={"pk": schedule.pk},
        ),
        data={
            "is_approve": new_approve,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_schedule_in_other_restaurant(
    api_client,
    manager,
):
    waiter = EmployeeFactory.create(role=Employee.Roles.WAITER)
    while waiter.restaurant.id == manager.restaurant.id:
        waiter = EmployeeFactory.create(role=Employee.Roles.WAITER)
    schedule = ScheduleFactory.create(employee=waiter)
    api_client.force_authenticate(user=manager.user)
    new_approve = not schedule.is_approve
    response = api_client.patch(
        reverse_lazy(
            "api:employeeSchedule-detail",
            kwargs={"pk": schedule.pk},
        ),
        data={
            "is_approve": new_approve,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_schedule_not_auth(
    api_client,
    manager,
):
    waiter = EmployeeFactory.create(role=Employee.Roles.WAITER)
    while waiter.restaurant.id == manager.restaurant.id:
        waiter = EmployeeFactory.create(role=Employee.Roles.WAITER)
    schedule = ScheduleFactory.create(employee=waiter)
    new_approve = not schedule.is_approve
    response = api_client.patch(
        reverse_lazy(
            "api:employeeSchedule-detail",
            kwargs={"pk": schedule.pk},
        ),
        data={
            "is_approve": new_approve,
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_destroy_schedule_manager(
    api_client,
    manager,
):
    waiter = EmployeeFactory.create(
        restaurant=manager.restaurant,
        role=Employee.Roles.WAITER,
    )
    schedule = ScheduleFactory.create(employee=waiter)
    api_client.force_authenticate(user=manager.user)
    response = api_client.delete(
        reverse_lazy(
            "api:employeeSchedule-detail",
            kwargs={"pk": schedule.pk},
        ),
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Schedule.objects.filter(pk=schedule.pk).exists()


def test_destroy_schedule_waiter(
    api_client,
    waiter,
):
    schedule = ScheduleFactory.create(employee=waiter)
    api_client.force_authenticate(user=waiter.user)
    response = api_client.delete(
        reverse_lazy(
            "api:employeeSchedule-detail",
            kwargs={"pk": schedule.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_destroy_schedule_in_other_restaurant(
    api_client,
    manager,
):
    waiter = EmployeeFactory.create(role=Employee.Roles.WAITER)
    while waiter.restaurant.id == manager.restaurant.id:
        waiter = EmployeeFactory.create(role=Employee.Roles.WAITER)
    schedule = ScheduleFactory.create(employee=waiter)
    api_client.force_authenticate(user=manager.user)
    response = api_client.delete(
        reverse_lazy(
            "api:employeeSchedule-detail",
            kwargs={"pk": schedule.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_destroy_schedule_not_auth(
    api_client,
    manager,
):
    waiter = EmployeeFactory.create(role=Employee.Roles.WAITER)
    while waiter.restaurant.id == manager.restaurant.id:
        waiter = EmployeeFactory.create(role=Employee.Roles.WAITER)
    schedule = ScheduleFactory.create(employee=waiter)
    response = api_client.delete(
        reverse_lazy(
            "api:employeeSchedule-detail",
            kwargs={"pk": schedule.pk},
        ),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
