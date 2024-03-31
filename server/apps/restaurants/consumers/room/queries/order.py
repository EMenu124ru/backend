from channels.db import database_sync_to_async
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.orders.functions import get_orders_by_restaurant as get_orders_by_restaurant_func
from apps.orders.models import Order


class OrderQueries:
    @staticmethod
    def get_orders_by_restaurant_sync(restaurant_id: int) -> QuerySet:
        return get_orders_by_restaurant_func(restaurant_id)

    @staticmethod
    @database_sync_to_async
    def get_orders_by_restaurant(restaurant_id: int) -> QuerySet:
        return OrderQueries.get_orders_by_restaurant_sync(restaurant_id)

    @staticmethod
    @database_sync_to_async
    def get_order(order_id: int) -> Order:
        return get_object_or_404(Order, id=order_id)
