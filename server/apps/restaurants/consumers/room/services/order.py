from collections import OrderedDict

from channels.db import database_sync_to_async
from django.db.models import QuerySet

from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer
from apps.users.models import Employee, User


class OrderService:

    @staticmethod
    @database_sync_to_async
    def get_orders_list(orders: QuerySet) -> list:
        orders = OrderSerializer(orders, many=True).data
        for order in orders:
            order['price'] = str(order['price'])
        return orders

    @staticmethod
    @database_sync_to_async
    def create_order(order: dict, employee: Employee) -> OrderedDict:
        serializer = OrderSerializer(data=order)
        serializer.is_valid(raise_exception=True)
        serializer.save(employee=employee)
        data = serializer.data
        data['price'] = str(data['price'])
        return data

    @staticmethod
    @database_sync_to_async
    def edit_order(body: dict, order: Order, user: User) -> OrderedDict:
        serializer = OrderSerializer(
            order,
            data=body,
            partial=True,
            context={"user": user},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        data['price'] = str(data['price'])
        return data
