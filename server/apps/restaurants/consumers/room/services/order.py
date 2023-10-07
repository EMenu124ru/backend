from channels.db import database_sync_to_async
from django.db.models import QuerySet

from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer


class OrderService:

    @staticmethod
    @database_sync_to_async
    def get_orders_list(orders: QuerySet) -> list:
        orders = OrderSerializer(orders, many=True).data
        for order in orders:
            order['price'] = float(order['price'])
        return orders

    @staticmethod
    @database_sync_to_async
    def create_order(order: dict, employee) -> list:
        serializer = OrderSerializer(data=order)
        serializer.is_valid(raise_exception=True)
        serializer.save(employee=employee)
        return serializer.data

    @staticmethod
    @database_sync_to_async
    def edit_order(body: dict, order: Order) -> list:
        serializer = OrderSerializer(order, data=body, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
