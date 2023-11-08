import pytest
from channels.db import database_sync_to_async
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.urls import path
from rest_framework_simplejwt.tokens import RefreshToken

from apps.core.middleware import JWTQueryParamAuthMiddleware
from apps.orders.factories import DishFactory, OrderAndDishFactory, OrderFactory
from apps.orders.models import Order, OrderAndDish
from apps.orders.serializers import OrderSerializer
from apps.restaurants.consumers import RestaurantConsumer
from apps.restaurants.factories import RestaurantFactory
from apps.users.factories import EmployeeFactory
from apps.users.models import Employee


@database_sync_to_async
def get_token(user) -> str:
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


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
async def test_connect_other_role(manager):
    token = await get_token(manager.user)
    restaurant = manager.restaurant
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
    cooking_orders = await database_sync_to_async(OrderFactory.create_batch)(
        size=2,
        status=Order.Statuses.COOKING,
        employee=waiter,
    )
    _ = await database_sync_to_async(OrderFactory.create_batch)(
        size=2,
        status=Order.Statuses.PAID,
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
    order_json = [dict(order) for order in (await get_serialized_orders(cooking_orders))]
    message = await communicator.receive_json_from()
    assert message == {"type": "list_orders", "body": {"orders": order_json}}
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_create_order_by_waiter(waiter):
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
    )
    order_json = await get_serialized_order(order)
    await communicator.send_json_to({"type": "create_order", "body": order_json})
    message = await communicator.receive_json_from()
    assert message["type"] == "new_order"
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
    )
    order_json = await get_serialized_order(order)
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
    body = {
        "id": order.id,
        "status": Order.Statuses.FINISHED,
    }
    await communicator.receive_json_from()
    await communicator.send_json_to({"type": "edit_order", "body": body})
    message = await communicator.receive_json_from()
    assert message["type"] == "order_changed"
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
    body = {
        "id": order.id,
        "status": Order.Statuses.FINISHED,
    }
    await communicator.receive_json_from()
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
    )
    await database_sync_to_async(OrderAndDishFactory.create_batch)(size=5, order=order)
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
    body = {
        "id": order.id,
        "dishes": [
            {"id": dish.id, "status": OrderAndDish.Statuses.DONE},
        ],
    }
    await communicator.receive_json_from()
    await communicator.send_json_to({"type": "edit_order", "body": body})
    message = await communicator.receive_json_from()
    assert message["type"] == "order_changed"
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_edit_order_waiter_add_dish(waiter):
    token = await get_token(waiter.user)
    restaurant = waiter.restaurant
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
    body = {
        "id": order.id,
        "dishes": [{"dish": dish.id}],
    }
    await communicator.receive_json_from()
    await communicator.send_json_to({"type": "edit_order", "body": body})
    message = await communicator.receive_json_from()
    assert message["type"] == "order_changed"
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
    body = {
        "id": order.id,
        "dishes": [{"dish": dish.id}],
    }
    await communicator.receive_json_from()
    await communicator.send_json_to({"type": "edit_order", "body": body})
    message = await communicator.receive_json_from()
    assert message["type"] == "error"
    await communicator.disconnect()
