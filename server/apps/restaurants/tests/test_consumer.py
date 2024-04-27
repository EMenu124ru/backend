import pytest
from channels.db import database_sync_to_async
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.urls import path

from apps.core.middleware import JWTQueryParamAuthMiddleware
from apps.core.utils import get_jwt_tokens
from apps.orders.factories import (
    DishFactory,
    OrderAndDishFactory,
    OrderFactory,
)
from apps.orders.functions import get_orders_by_restaurant
from apps.orders.models import Order, OrderAndDish
from apps.orders.serializers import OrderAndDishSerializer, OrderSerializer
from apps.restaurants.consumers import RestaurantConsumer
from apps.restaurants.factories import PlaceFactory, RestaurantFactory
from apps.users.factories import EmployeeFactory
from apps.users.models import Employee


@database_sync_to_async
def get_token(user) -> str:
    return get_jwt_tokens(user)["access"]


@database_sync_to_async
def get_serialized_orders(orders):
    orders = OrderSerializer(orders, many=True).data
    for order in orders:
        order['price'] = str(order['price'])
    return orders


@database_sync_to_async
def get_serialized_order(order):
    order = OrderSerializer(order).data
    order['price'] = str(order['price'])
    return order


@database_sync_to_async
def get_serialized_order_and_dishes(dishes):
    return OrderAndDishSerializer(dishes).data


@database_sync_to_async
def get_order_ids(orders):
    return sorted([order.id for order in orders])


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_connect_waiter(waiter):
    token = await get_token(waiter.user)
    restaurant = waiter.restaurant
    application = JWTQueryParamAuthMiddleware(URLRouter([
        path("ws/restaurant/<restaurant_id>/", RestaurantConsumer.as_asgi()),
    ]))
    communicator = WebsocketCommunicator(
        application,
        f"ws/restaurant/{restaurant.id}/?token={token}",
    )
    connected, _ = await communicator.connect()
    assert connected
    message = await communicator.receive_json_from()
    assert message["type"] == "list_orders"
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_connect_chef(chef):
    token = await get_token(chef.user)
    restaurant = chef.restaurant
    application = JWTQueryParamAuthMiddleware(URLRouter([
        path("ws/restaurant/<restaurant_id>/", RestaurantConsumer.as_asgi()),
    ]))
    communicator = WebsocketCommunicator(
        application,
        f"ws/restaurant/{restaurant.id}/?token={token}",
    )
    connected, _ = await communicator.connect()
    assert connected
    message = await communicator.receive_json_from()
    assert message["type"] == "list_orders"
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_connect_other_role(hostess):
    token = await get_token(hostess.user)
    restaurant = hostess.restaurant
    application = JWTQueryParamAuthMiddleware(URLRouter([
        path("ws/restaurant/<restaurant_id>/", RestaurantConsumer.as_asgi()),
    ]))
    communicator = WebsocketCommunicator(
        application,
        f"ws/restaurant/{restaurant.id}/?token={token}",
    )

    connected, _ = await communicator.connect()
    assert connected
    message = await communicator.receive_json_from()
    assert message == {"type": "error", 'detail': 'Employee has wrong role'}
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_connect_not_auth():
    restaurant = await database_sync_to_async(RestaurantFactory.create)()
    application = JWTQueryParamAuthMiddleware(URLRouter([
        path("ws/restaurant/<restaurant_id>/", RestaurantConsumer.as_asgi()),
    ]))
    communicator = WebsocketCommunicator(
        application,
        f"ws/restaurant/{restaurant.id}/",
    )
    connected, _ = await communicator.connect()
    assert connected
    message = await communicator.receive_json_from()
    assert message == {"type": "error", 'detail': "User isn't authenticated"}
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_connect_not_consists_employee(waiter):
    token = await get_token(waiter.user)
    restaurant = await database_sync_to_async(RestaurantFactory.create)()
    application = JWTQueryParamAuthMiddleware(URLRouter([
        path("ws/restaurant/<restaurant_id>/", RestaurantConsumer.as_asgi()),
    ]))
    communicator = WebsocketCommunicator(
        application,
        f"ws/restaurant/{restaurant.id}/?token={token}",
    )
    connected, _ = await communicator.connect()
    assert connected
    message = await communicator.receive_json_from()
    assert message == {"type": "error", 'detail': "Employee isn't member of restaurant"}
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_connect_client(client):
    token = await get_token(client.user)
    restaurant = await database_sync_to_async(RestaurantFactory.create)()
    application = JWTQueryParamAuthMiddleware(URLRouter([
        path("ws/restaurant/<restaurant_id>/", RestaurantConsumer.as_asgi()),
    ]))
    communicator = WebsocketCommunicator(
        application,
        f"ws/restaurant/{restaurant.id}/?token={token}",
    )
    connected, _ = await communicator.connect()
    assert connected
    message = await communicator.receive_json_from()
    assert message == {"type": "error", 'detail': "User isn't employee"}
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_connect_wrong_restaurant_id(waiter):
    token = await get_token(waiter.user)
    application = JWTQueryParamAuthMiddleware(URLRouter([
        path("ws/restaurant/<restaurant_id>/", RestaurantConsumer.as_asgi()),
    ]))
    communicator = WebsocketCommunicator(
        application,
        f"ws/restaurant/some_key/?token={token}",
    )
    connected, _ = await communicator.connect()
    assert connected
    message = await communicator.receive_json_from()
    assert message == {"type": "error", 'detail': "Enter right primary key of restaurant"}

    communicator = WebsocketCommunicator(
        application,
        f"ws/restaurant/0/?token={token}",
    )
    connected, _ = await communicator.connect()
    assert connected
    message = await communicator.receive_json_from()
    assert message == {"type": "error", 'detail': "Restaurant doesn't exists"}
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_employee_orders_list(waiter):
    token = await get_token(waiter.user)
    restaurant = waiter.restaurant

    waiting_for_cooking_orders = await database_sync_to_async(OrderFactory.create_batch)(
        size=2,
        status=Order.Statuses.WAITING_FOR_COOKING,
        employee=waiter,
    )
    cooking_orders = await database_sync_to_async(OrderFactory.create_batch)(
        size=2,
        status=Order.Statuses.COOKING,
        employee=waiter,
    )
    waiting_for_delivery_orders = await database_sync_to_async(OrderFactory.create_batch)(
        size=2,
        status=Order.Statuses.WAITING_FOR_DELIVERY,
        employee=waiter,
    )
    in_process_delivery_orders = await database_sync_to_async(OrderFactory.create_batch)(
        size=2,
        status=Order.Statuses.IN_PROCESS_DELIVERY,
        employee=waiter,
    )
    delivered_orders = await database_sync_to_async(OrderFactory.create_batch)(
        size=2,
        status=Order.Statuses.DELIVERED,
        employee=waiter,
    )
    paid_orders = await database_sync_to_async(OrderFactory.create_batch)(
        size=2,
        status=Order.Statuses.PAID,
        employee=waiter,
    )
    created_orders = [
        *waiting_for_cooking_orders,
        *cooking_orders,
        *waiting_for_delivery_orders,
        *in_process_delivery_orders,
        *delivered_orders,
        *paid_orders,
    ]
    created_order_ids = sorted([order.id for order in created_orders])
    application = JWTQueryParamAuthMiddleware(URLRouter([
        path("ws/restaurant/<restaurant_id>/", RestaurantConsumer.as_asgi()),
    ]))
    communicator = WebsocketCommunicator(
        application,
        f"ws/restaurant/{restaurant.id}/?token={token}",
    )
    orders = await database_sync_to_async(get_orders_by_restaurant)(restaurant.id)
    orders_ids = await get_order_ids(orders)
    connected, _ = await communicator.connect()
    assert connected
    orders_json = [
        dict(order)
        for order in (await get_serialized_orders(orders))
    ]
    orders_json.sort(key=lambda obj: obj["status"])
    message = await communicator.receive_json_from()
    assert created_order_ids == orders_ids
    assert message == {"type": "list_orders", "body": {"orders": orders_json}}
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_create_order_by_waiter_without_dishes_failed(waiter):
    token = await get_token(waiter.user)
    restaurant = waiter.restaurant
    application = JWTQueryParamAuthMiddleware(URLRouter([
        path("ws/restaurant/<restaurant_id>/", RestaurantConsumer.as_asgi()),
    ]))
    communicator = WebsocketCommunicator(
        application,
        f"ws/restaurant/{restaurant.id}/?token={token}",
    )
    connected, _ = await communicator.connect()
    assert connected
    await communicator.receive_json_from()
    order = await database_sync_to_async(OrderFactory.build)(
        status=Order.Statuses.WAITING_FOR_COOKING,
        employee=None,
        reservation=None,
    )
    order_json = {
        "price": str(order.price),
        "status": order.status,
        "comment": order.comment,
        "client": order.client.pk if order.client else None,
        "employee": order.employee,
        "reservation": order.reservation,
        "dishes": [],
    }
    await communicator.send_json_to({"type": "create_order", "body": order_json})
    message = await communicator.receive_json_from()
    assert message["type"] == "error"
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_create_order_by_waiter_not_by_websocket(waiter):
    token = await get_token(waiter.user)
    restaurant = waiter.restaurant
    application = JWTQueryParamAuthMiddleware(URLRouter([
        path("ws/restaurant/<restaurant_id>/", RestaurantConsumer.as_asgi()),
    ]))
    communicator = WebsocketCommunicator(
        application,
        f"ws/restaurant/{restaurant.id}/?token={token}",
    )
    connected, _ = await communicator.connect()
    assert connected
    await communicator.receive_json_from()
    await database_sync_to_async(OrderFactory.create)(
        status=Order.Statuses.WAITING_FOR_COOKING,
        employee=waiter,
        reservation=None,
    )
    message = await communicator.receive_json_from()
    assert message["type"] == "list_orders"
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_create_order_by_waiter_without_dishes_without_reservation(waiter):
    token = await get_token(waiter.user)
    restaurant = waiter.restaurant
    application = JWTQueryParamAuthMiddleware(URLRouter([
        path("ws/restaurant/<restaurant_id>/", RestaurantConsumer.as_asgi()),
    ]))
    communicator = WebsocketCommunicator(
        application,
        f"ws/restaurant/{restaurant.id}/?token={token}",
    )
    connected, _ = await communicator.connect()
    assert connected
    await communicator.receive_json_from()
    order = await database_sync_to_async(OrderFactory.build)(
        status=Order.Statuses.WAITING_FOR_COOKING,
        employee=None,
        reservation=None,
    )
    dishes = await database_sync_to_async(DishFactory.create_batch)(size=2)
    order_json = {
        "price": str(order.price),
        "status": order.status,
        "comment": order.comment,
        "client": order.client.pk if order.client else None,
        "employee": order.employee,
        "dishes": [{"dish": dish.pk} for dish in dishes],
    }
    await communicator.send_json_to({"type": "create_order", "body": order_json})
    message = await communicator.receive_json_from()
    assert message["type"] == "error"
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_create_order_by_waiter_without_dishes(waiter):
    token = await get_token(waiter.user)
    restaurant = waiter.restaurant
    application = JWTQueryParamAuthMiddleware(URLRouter([
        path("ws/restaurant/<restaurant_id>/", RestaurantConsumer.as_asgi()),
    ]))
    communicator = WebsocketCommunicator(
        application,
        f"ws/restaurant/{restaurant.id}/?token={token}",
    )
    connected, _ = await communicator.connect()
    assert connected
    await communicator.receive_json_from()
    order = await database_sync_to_async(OrderFactory.build)(
        status=Order.Statuses.WAITING_FOR_COOKING,
        employee=None,
        reservation=None,
    )
    place = await database_sync_to_async(PlaceFactory.create)(restaurant=waiter.restaurant)
    dishes = await database_sync_to_async(DishFactory.create_batch)(size=2)
    order_json = {
        "price": str(order.price),
        "status": order.status,
        "comment": order.comment,
        "client": order.client.pk if order.client else None,
        "employee": order.employee,
        "place": place.pk,
        "dishes": [{"dish": dish.pk} for dish in dishes],
    }
    await communicator.send_json_to({"type": "create_order", "body": order_json})
    message = await communicator.receive_json_from()
    assert message["type"] == "list_orders"
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_create_order_by_chef(chef):
    token = await get_token(chef.user)
    restaurant = chef.restaurant
    application = JWTQueryParamAuthMiddleware(URLRouter([
        path("ws/restaurant/<restaurant_id>/", RestaurantConsumer.as_asgi()),
    ]))
    communicator = WebsocketCommunicator(
        application,
        f"ws/restaurant/{restaurant.id}/?token={token}",
    )
    connected, _ = await communicator.connect()
    assert connected
    await communicator.receive_json_from()
    order = await database_sync_to_async(OrderFactory.build)(
        status=Order.Statuses.WAITING_FOR_COOKING,
        employee=None,
        reservation=None,
    )
    order_json = {
        "price": str(order.price),
        "status": order.status,
        "comment": order.comment,
        "client": order.client.pk if order.client else None,
        "employee": order.employee,
        "reservation": order.reservation,
        "dishes": [],
    }
    await communicator.send_json_to({"type": "create_order", "body": order_json})
    message = await communicator.receive_json_from()
    assert message["type"] == "error"
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_edit_order_waiter(waiter):
    token = await get_token(waiter.user)
    restaurant = waiter.restaurant
    order = await database_sync_to_async(OrderFactory.create)(
        status=Order.Statuses.COOKING,
        employee=waiter,
        reservation=None,
    )
    application = JWTQueryParamAuthMiddleware(URLRouter([
        path("ws/restaurant/<restaurant_id>/", RestaurantConsumer.as_asgi()),
    ]))
    communicator = WebsocketCommunicator(
        application,
        f"ws/restaurant/{restaurant.id}/?token={token}",
    )
    connected, _ = await communicator.connect()
    assert connected
    await communicator.receive_json_from()
    body = {
        "id": order.id,
        "status": Order.Statuses.FINISHED,
    }
    await communicator.send_json_to({"type": "edit_order", "body": body})
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_edit_order_chef_failed(chef):
    token = await get_token(chef.user)
    restaurant = chef.restaurant
    waiter = await database_sync_to_async(EmployeeFactory.create)(
        role=Employee.Roles.WAITER,
        restaurant=restaurant,
    )
    order = await database_sync_to_async(OrderFactory.create)(
        status=Order.Statuses.COOKING,
        employee=waiter,
    )
    application = JWTQueryParamAuthMiddleware(URLRouter([
        path("ws/restaurant/<restaurant_id>/", RestaurantConsumer.as_asgi()),
    ]))
    communicator = WebsocketCommunicator(
        application,
        f"ws/restaurant/{restaurant.id}/?token={token}",
    )
    connected, _ = await communicator.connect()
    assert connected
    await communicator.receive_json_from()
    body = {
        "id": order.id,
        "status": Order.Statuses.FINISHED,
    }
    await communicator.send_json_to({"type": "edit_order", "body": body})
    message = await communicator.receive_json_from()
    assert message["type"] == "error"
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_edit_order_chef_success(chef):
    token = await get_token(chef.user)
    restaurant = chef.restaurant
    waiter = await database_sync_to_async(EmployeeFactory.create)(
        role=Employee.Roles.WAITER,
        restaurant=restaurant,
    )
    order = await database_sync_to_async(OrderFactory.create)(
        status=Order.Statuses.COOKING,
        employee=waiter,
        reservation=None,
    )
    await database_sync_to_async(OrderAndDishFactory.create_batch)(
        size=5,
        order=order,
        status=OrderAndDish.Statuses.COOKING,
    )
    application = JWTQueryParamAuthMiddleware(URLRouter([
        path("ws/restaurant/<restaurant_id>/", RestaurantConsumer.as_asgi()),
    ]))
    communicator = WebsocketCommunicator(
        application,
        f"ws/restaurant/{restaurant.id}/?token={token}",
    )
    connected, _ = await communicator.connect()
    assert connected
    dish = await database_sync_to_async(order.dishes.first)()
    await communicator.receive_json_from()
    body = {
        "id": order.id,
        "dishes": [
            {"id": dish.id, "status": OrderAndDish.Statuses.DONE},
        ],
    }
    await communicator.send_json_to({"type": "edit_order", "body": body})
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_edit_order_waiter_add_dish(waiter):
    token = await get_token(waiter.user)
    restaurant = waiter.restaurant
    order = await database_sync_to_async(OrderFactory.create)(
        status=Order.Statuses.COOKING,
        employee=waiter,
        reservation=None,
    )
    dish = await database_sync_to_async(DishFactory.create)()
    application = JWTQueryParamAuthMiddleware(URLRouter([
        path("ws/restaurant/<restaurant_id>/", RestaurantConsumer.as_asgi()),
    ]))
    communicator = WebsocketCommunicator(
        application,
        f"ws/restaurant/{restaurant.id}/?token={token}",
    )
    connected, _ = await communicator.connect()
    assert connected
    await communicator.receive_json_from()
    body = {
        "id": order.id,
        "dishes": [{"dish": dish.id}],
    }
    await communicator.send_json_to({"type": "edit_order", "body": body})
    message = await communicator.receive_json_from()
    assert message["type"] == "list_orders"
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_edit_order_chef_add_dish(chef):
    token = await get_token(chef.user)
    restaurant = chef.restaurant
    waiter = await database_sync_to_async(EmployeeFactory.create)(
        role=Employee.Roles.WAITER,
        restaurant=restaurant,
    )
    order = await database_sync_to_async(OrderFactory.create)(
        status=Order.Statuses.COOKING,
        employee=waiter,
    )
    dish = await database_sync_to_async(DishFactory.create)()
    application = JWTQueryParamAuthMiddleware(URLRouter([
        path("ws/restaurant/<restaurant_id>/", RestaurantConsumer.as_asgi()),
    ]))
    communicator = WebsocketCommunicator(
        application,
        f"ws/restaurant/{restaurant.id}/?token={token}",
    )
    connected, _ = await communicator.connect()
    assert connected
    await communicator.receive_json_from()
    body = {
        "id": order.id,
        "dishes": [{"dish": dish.id}],
    }
    await communicator.send_json_to({"type": "edit_order", "body": body})
    message = await communicator.receive_json_from()
    assert message["type"] == "error"
    await communicator.disconnect()
