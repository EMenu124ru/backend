import pytest
# from django.urls import reverse_lazy
# from rest_framework import status

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