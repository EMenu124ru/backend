from datetime import datetime, timedelta

import pytest
import pytz
from django.urls import reverse_lazy
from rest_framework import status

from apps.orders.factories import OrderFactory, ReservationFactory, DishFactory
from apps.orders.models import Reservation
from apps.restaurants.factories import PlaceFactory, RestaurantFactory
from apps.users.factories import ClientFactory

pytestmark = pytest.mark.django_db

DISH_COUNT = 4


def test_create_reservation_by_waiter(
    waiter,
    api_client,
) -> None:
    restaurant = waiter.restaurant
    place = PlaceFactory.create(restaurant=restaurant)
    reservation = ReservationFactory.build(
        restaurant=restaurant,
        place=place,
    )
    api_client.force_authenticate(user=waiter.user)
    response = api_client.post(
        reverse_lazy("api:reservations-list"),
        data={
            "restaurant": reservation.restaurant.pk,
            "arrival_time": reservation.arrival_time,
            "place": reservation.place.pk,
        },
        format='json',
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_read_reservation_by_waiter(
    waiter,
    api_client,
) -> None:
    reservation = ReservationFactory.create(restaurant=waiter.restaurant)
    api_client.force_authenticate(user=waiter.user)
    response = api_client.get(
        reverse_lazy(
            "api:reservations-detail",
            kwargs={"pk": reservation.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_update_reservation_by_waiter_failed(
    waiter,
    api_client,
) -> None:
    restaurant = waiter.restaurant
    place = PlaceFactory.create(restaurant=restaurant)
    reservation = ReservationFactory.create(
        restaurant=restaurant,
        place=place,
        status=Reservation.Statuses.OPENED,
    )
    api_client.force_authenticate(user=waiter.user)
    new_arrival_time = reservation.arrival_time + timedelta(seconds=60*60)
    response = api_client.patch(
        reverse_lazy(
            "api:reservations-detail",
            kwargs={"pk": reservation.pk},
        ),
        data={
            "arrival_time": new_arrival_time,
        },
        format='json',
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Reservation.objects.filter(
        id=reservation.pk,
        arrival_time=reservation.arrival_time,
    ).exists()


def test_update_reservation_by_waiter_success(
    waiter,
    api_client,
) -> None:
    place = PlaceFactory.create(restaurant=waiter.restaurant)
    reservation = ReservationFactory.create(
        restaurant=waiter.restaurant,
        place=place,
        status=Reservation.Statuses.OPENED,
    )
    api_client.force_authenticate(user=waiter.user)
    new_place = PlaceFactory.create(restaurant=waiter.restaurant)
    new_status = Reservation.Statuses.FINISHED
    response = api_client.patch(
        reverse_lazy(
            "api:reservations-detail",
            kwargs={"pk": reservation.pk},
        ),
        data={
            "place": new_place.pk,
            "status": new_status,
        },
        format='json',
    )
    assert response.status_code == status.HTTP_200_OK
    assert Reservation.objects.filter(
        id=reservation.pk,
        place=new_place,
        status=new_status,
    ).exists()


def test_update_reservation_by_waiter_set_other_place_other_restaurant(
    waiter,
    api_client,
) -> None:
    place = PlaceFactory.create(restaurant=waiter.restaurant)
    reservation = ReservationFactory.create(
        restaurant=waiter.restaurant,
        place=place,
        status=Reservation.Statuses.OPENED,
    )
    api_client.force_authenticate(user=waiter.user)
    new_place = PlaceFactory.create()
    while new_place.restaurant.id == reservation.place.restaurant.id:
        new_place = PlaceFactory.create()
    response = api_client.patch(
        reverse_lazy(
            "api:reservations-detail",
            kwargs={"pk": reservation.pk},
        ),
        data={
            "place": new_place.pk,
        },
        format='json',
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Reservation.objects.filter(
        id=reservation.pk,
        place=reservation.place,
    ).exists()


def test_update_reservation_by_waiter_reopened_finish(
    waiter,
    api_client,
) -> None:
    reservation = ReservationFactory.create(
        restaurant=waiter.restaurant,
        status=Reservation.Statuses.FINISHED,
    )
    api_client.force_authenticate(user=waiter.user)
    new_status = Reservation.Statuses.OPENED
    response = api_client.patch(
        reverse_lazy(
            "api:reservations-detail",
            kwargs={"pk": reservation.pk},
        ),
        data={
            "status": new_status,
        },
        format='json',
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Reservation.objects.filter(
        id=reservation.pk,
        status=reservation.status,
    ).exists()


def test_update_reservation_by_waiter_reopened_canceled(
    waiter,
    api_client,
) -> None:
    reservation = ReservationFactory.create(
        restaurant=waiter.restaurant,
        status=Reservation.Statuses.CANCELED,
    )
    api_client.force_authenticate(user=waiter.user)
    new_status = Reservation.Statuses.OPENED
    response = api_client.patch(
        reverse_lazy(
            "api:reservations-detail",
            kwargs={"pk": reservation.pk},
        ),
        data={
            "status": new_status,
        },
        format='json',
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Reservation.objects.filter(
        id=reservation.pk,
        status=reservation.status,
    ).exists()


def test_update_reservation_by_waiter_from_other_restaurant(
    waiter,
    api_client,
) -> None:
    restaurant = RestaurantFactory.create()
    place = PlaceFactory.create(restaurant=restaurant)
    reservation = ReservationFactory.create(
        restaurant=restaurant,
        place=place,
        status=Reservation.Statuses.OPENED,
    )
    api_client.force_authenticate(user=waiter.user)
    new_client = ClientFactory.create()
    response = api_client.patch(
        reverse_lazy(
            "api:reservations-detail",
            kwargs={"pk": reservation.pk},
        ),
        data={
            "client": new_client.pk,
        },
        format='json',
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Reservation.objects.filter(
        id=reservation.pk,
        client=reservation.client,
    ).exists()


def test_create_reservation_by_client_success(
    client,
    api_client,
) -> None:
    restaurant = RestaurantFactory.create()
    place = PlaceFactory.create(restaurant=restaurant)
    reservation = ReservationFactory.build(
        restaurant=restaurant,
        place=place,
    )
    api_client.force_authenticate(user=client.user)
    response = api_client.post(
        reverse_lazy("api:reservations-list"),
        data={
            "restaurant": reservation.restaurant.pk,
            "arrival_time": reservation.arrival_time,
        },
        format='json',
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Reservation.objects.filter(
        restaurant=restaurant.pk,
        arrival_time=reservation.arrival_time,
    ).exists()


def test_create_reservation_by_client_success_with_order(
    client,
    api_client,
) -> None:
    restaurant = RestaurantFactory.create()
    place = PlaceFactory.create(restaurant=restaurant)
    reservation = ReservationFactory.build(
        restaurant=restaurant,
        place=place,
    )
    order = OrderFactory.build()
    dish = DishFactory.create()
    order_dict = {
        "status": order.status,
        "comment": order.comment,
        "client": client.pk,
        "dishes": [{"dish": dish.id, "comment": "some comment"}],
    }
    api_client.force_authenticate(user=client.user)
    response = api_client.post(
        reverse_lazy("api:reservations-list"),
        data={
            "restaurant": reservation.restaurant.pk,
            "arrival_time": reservation.arrival_time,
            "order": order_dict,
        },
        format='json',
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Reservation.objects.filter(
        restaurant=restaurant.pk,
        arrival_time=reservation.arrival_time,
    ).exists()
    assert Reservation.objects.get(
        restaurant=restaurant.pk,
        arrival_time=reservation.arrival_time,
    ).orders.exists()


def test_create_reservation_by_client_failed_place(
    client,
    api_client,
) -> None:
    restaurant = RestaurantFactory.create()
    place = PlaceFactory.create(restaurant=restaurant)
    reservation = ReservationFactory.build(
        restaurant=restaurant,
        place=place,
    )
    api_client.force_authenticate(user=client.user)
    response = api_client.post(
        reverse_lazy("api:reservations-list"),
        data={
            "restaurant": reservation.restaurant.pk,
            "arrival_time": reservation.arrival_time,
            "place": reservation.place.pk,
        },
        format='json',
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_reservation_by_client_failed(
    client,
    api_client,
) -> None:
    restaurant = RestaurantFactory.create()
    reservation = ReservationFactory.create(
        client=client,
        restaurant=restaurant,
        status=Reservation.Statuses.OPENED,
    )
    new_place = PlaceFactory.create(
        restaurant=restaurant,
    )
    api_client.force_authenticate(user=client.user)
    response = api_client.patch(
        reverse_lazy(
            "api:reservations-detail",
            kwargs={"pk": reservation.pk},
        ),
        data={
            "place": new_place.pk,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Reservation.objects.filter(
        pk=reservation.pk,
        place=reservation.place,
    )


def test_read_reservation_by_client_success(
    client,
    api_client,
) -> None:
    restaurant = RestaurantFactory.create()
    reservation = ReservationFactory.create(
        client=client,
        restaurant=restaurant,
    )
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
        reverse_lazy(
            "api:reservations-detail",
            kwargs={"pk": reservation.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_reservation_by_client_failed(
    client,
    api_client,
) -> None:
    reservation = ReservationFactory.create(
        client=ClientFactory.create(),
    )
    api_client.force_authenticate(user=client.user)
    response = api_client.get(
        reverse_lazy(
            "api:reservations-detail",
            kwargs={"pk": reservation.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_reservation_by_hostess_success(
    hostess,
    api_client,
) -> None:
    place = PlaceFactory.create(restaurant=hostess.restaurant)
    reservation = ReservationFactory.build(
        restaurant=hostess.restaurant,
        place=place,
    )
    api_client.force_authenticate(user=hostess.user)
    response = api_client.post(
        reverse_lazy("api:reservations-list"),
        data={
            "restaurant": reservation.restaurant.pk,
            "arrival_time": reservation.arrival_time,
            "place": reservation.place.pk,
        },
        format='json',
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_create_reservation_by_hostess_failed(
    hostess,
    client,
    api_client,
) -> None:
    place = PlaceFactory.create(restaurant=hostess.restaurant)
    reservation = ReservationFactory.build(
        restaurant=hostess.restaurant,
        place=place,
    )
    order = OrderFactory.build()
    dish = DishFactory.create()
    order_dict = {
        "status": order.status,
        "comment": order.comment,
        "client": client.pk,
        "dishes": [{"dish": dish.id, "comment": "some comment"}],
    }
    api_client.force_authenticate(user=hostess.user)
    response = api_client.post(
        reverse_lazy("api:reservations-list"),
        data={
            "restaurant": reservation.restaurant.pk,
            "arrival_time": reservation.arrival_time,
            "place": reservation.place.pk,
            "order": order_dict,
        },
        format='json',
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_reservation_by_hostess_success(
    hostess,
    api_client,
) -> None:
    place = PlaceFactory.create(restaurant=hostess.restaurant)
    reservation = ReservationFactory.create(
        restaurant=hostess.restaurant,
        place=place,
        status=Reservation.Statuses.OPENED,
    )
    api_client.force_authenticate(user=hostess.user)
    new_place = PlaceFactory.create(restaurant=hostess.restaurant)
    new_arrival_time = datetime.now(pytz.UTC) + timedelta(days=3)
    response = api_client.patch(
        reverse_lazy(
            "api:reservations-detail",
            kwargs={"pk": reservation.pk},
        ),
        data={
            "place": new_place.pk,
            "arrival_time": new_arrival_time,
            "status": Reservation.Statuses.FINISHED,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert Reservation.objects.filter(
        id=reservation.pk,
        place_id=new_place.pk,
        arrival_time=new_arrival_time,
        status=Reservation.Statuses.FINISHED,
    ).exists()


def test_update_reservation_by_hostess_failed(
    hostess,
    api_client,
) -> None:
    place = PlaceFactory.create(restaurant=hostess.restaurant)
    reservation = ReservationFactory.create(
        restaurant=hostess.restaurant,
        place=place,
        status=Reservation.Statuses.OPENED,
    )
    api_client.force_authenticate(user=hostess.user)
    new_restaurant = RestaurantFactory.create()
    response = api_client.patch(
        reverse_lazy(
            "api:reservations-detail",
            kwargs={"pk": reservation.pk},
        ),
        data={
            "restaurant": new_restaurant.pk,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_reservation_by_unauthorized(
    api_client,
) -> None:
    restaurant = RestaurantFactory.build()
    place = PlaceFactory.build(restaurant=restaurant)
    reservation = ReservationFactory.build(
        restaurant=restaurant,
        place=place,
    )
    response = api_client.post(
        reverse_lazy("api:reservations-list"),
        data={
            "restaurant": reservation.restaurant.pk,
            "arrival_time": reservation.arrival_time,
            "place": reservation.place.pk,
        },
        format='json',
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_read_reservation_by_unauthorized(
    api_client,
) -> None:
    reservation = ReservationFactory.create()
    response = api_client.get(
        reverse_lazy(
            "api:reservations-detail",
            kwargs={"pk": reservation.pk},
        ),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_reservation_by_unauthorized(
    api_client,
) -> None:
    reservation = ReservationFactory.create()
    new_order = OrderFactory.create()
    response = api_client.patch(
        reverse_lazy(
            "api:reservations-detail",
            kwargs={"pk": reservation.pk},
        ),
        data={
            "order": new_order,
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
