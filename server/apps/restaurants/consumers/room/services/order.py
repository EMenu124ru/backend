from channels.db import database_sync_to_async
from django.db.models import QuerySet

from apps.orders.serializers import OrderSerializer


class OrderService:

    @staticmethod
    @database_sync_to_async
    def get_orders_list(orders: QuerySet) -> list:
        return OrderSerializer(orders, many=True).data
