import pytest
from django.urls import reverse_lazy
from rest_framework import status

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
    api_client
) -> None:
    api_client.force_authenticate()
    response = api_client.get(reverse_lazy("api:staff-detail"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
