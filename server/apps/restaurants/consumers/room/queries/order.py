from channels.db import database_sync_to_async
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.orders.models import Order


class OrderQueries:

    @staticmethod
    @database_sync_to_async
    def get_orders_by_restaurant(restaurant_id: int) -> QuerySet:
        access_status = [
            Order.Statuses.WAITING_FOR_COOKING,
            Order.Statuses.COOKING,
            Order.Statuses.WAITING_FOR_DELIVERY,
            Order.Statuses.IN_PROCESS_DELIVERY,
            Order.Statuses.DELIVERED,
        ]
        return Order.objects.filter(
            employee__restaurant_id=restaurant_id,
            status__in=access_status,
        ).all()
    
    @staticmethod
    @database_sync_to_async
    def get_order(order_id: int) -> Order:
        return get_object_or_404(Order, id=order_id)
