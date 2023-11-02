import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.users.factories import EmployeeFactory

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
