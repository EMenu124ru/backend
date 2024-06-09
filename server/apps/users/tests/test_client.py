import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.users.factories import ClientFactory
from apps.users.models import Client, User

pytestmark = pytest.mark.django_db


def test_create_client_without_surname(
    api_client,
) -> None:
    client = ClientFactory.build(user__phone_number="+7999999999")
    response = api_client.post(
        reverse_lazy("api:clients-list"),
        data={
            "first_name": client.user.first_name,
            "last_name": client.user.last_name,
            "password": client.user.password,
            "bonuses": client.bonuses,
            "phone_number": client.user.phone_number,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Client.objects.filter(
        id=response.data["id"],
        bonuses=client.bonuses,
    ).exists()


def test_create_client_with_same_info(
    api_client,
) -> None:
    client = ClientFactory.build(user__phone_number="+7999999999")
    response = api_client.post(
        reverse_lazy("api:clients-list"),
        data={
            "first_name": client.user.first_name,
            "last_name": client.user.last_name,
            "password": client.user.password,
            "bonuses": client.bonuses,
            "phone_number": client.user.phone_number,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Client.objects.filter(
        id=response.data["id"],
        bonuses=client.bonuses,
    ).exists()
    response = api_client.post(
        reverse_lazy("api:clients-list"),
        data={
            "first_name": client.user.first_name,
            "last_name": client.user.last_name,
            "password": client.user.password,
            "bonuses": client.bonuses,
            "phone_number": client.user.phone_number,
        },
    )
    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE


def test_create_client_with_surname(
    api_client,
) -> None:
    client = ClientFactory.build(user__phone_number="+7999999999")
    response = api_client.post(
        reverse_lazy("api:clients-list"),
        data={
            "first_name": client.user.first_name,
            "last_name": client.user.last_name,
            "surname": client.user.surname,
            "password": client.user.password,
            "bonuses": client.bonuses,
            "phone_number": client.user.phone_number,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Client.objects.filter(
        id=response.data["id"],
        bonuses=client.bonuses,
    ).exists()


def test_get_client_own(
    client,
    api_client,
) -> None:
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
        reverse_lazy(
            "api:clients-detail",
            kwargs={"pk": client.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == client.id


def test_get_me_client(
    client,
    api_client
) -> None:
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
        reverse_lazy("api:clients-me"),
    )
    assert response.status_code == status.HTTP_200_OK


def test_get_client_other(
    client,
    api_client,
) -> None:
    client_own = ClientFactory.create()
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
        reverse_lazy(
            "api:clients-detail",
            kwargs={"pk": client_own.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_client_not_auth(
    client,
    api_client,
) -> None:
    response = api_client.get(
        reverse_lazy(
            "api:clients-detail",
            kwargs={"pk": client.pk},
        ),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_me_client_not_auth(
    api_client
) -> None:
    api_client.force_authenticate()
    response = api_client.get(
        reverse_lazy("api:clients-me"),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_client_own_password(
    client,
    api_client
) -> None:
    api_client.force_authenticate(user=client.user)
    new_password = "new_password"
    response = api_client.patch(
        reverse_lazy(
            "api:clients-detail",
            kwargs={"pk": client.pk},
        ),
        data={
            "password": new_password,
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert Client.objects.get(pk=client.pk).user.check_password(new_password)


def test_update_client_own(
    client,
    api_client
) -> None:
    api_client.force_authenticate(user=client.user)
    new_phone_number = "+78005553535"
    response = api_client.patch(
        reverse_lazy(
            "api:clients-detail",
            kwargs={"pk": client.pk},
        ),
        data={
            "phone_number": new_phone_number,
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert Client.objects.get(pk=client.pk).user.phone_number == new_phone_number


def test_update_client_other(
    client,
    api_client
) -> None:
    other_client = ClientFactory.create()
    api_client.force_authenticate(user=client.user)
    new_phone_number = "+88005553535"
    response = api_client.patch(
        reverse_lazy(
            "api:clients-detail",
            kwargs={"pk": other_client.pk},
        ),
        data={
            "phone_number": new_phone_number,
        }
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_client_not_auth(
    client,
    api_client
) -> None:
    new_bonuses = client.bonuses + 1000
    response = api_client.patch(
        reverse_lazy(
            "api:clients-detail",
            kwargs={"pk": client.pk},
        ),
        data={
            "bonuses": new_bonuses,
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_remove_client_own(
    client,
    api_client
) -> None:
    user_id = client.user.pk
    api_client.force_authenticate(user=client.user)
    response = api_client.delete(
        reverse_lazy(
            "api:clients-detail",
            kwargs={"pk": client.pk},
        ),
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Client.objects.filter(
        pk=client.pk,
    ).exists()
    assert not User.objects.filter(pk=user_id).exists()


def test_remove_client_other(
    client,
    api_client
) -> None:
    other_client = ClientFactory.create()
    api_client.force_authenticate(user=client.user)
    response = api_client.delete(
        reverse_lazy(
            "api:clients-detail",
            kwargs={"pk": other_client.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_remove_client_not_auth(
    client,
    api_client
) -> None:
    response = api_client.delete(
        reverse_lazy(
            "api:clients-detail",
            kwargs={"pk": client.pk},
        ),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
