from channels.db import database_sync_to_async
from django.db.models import QuerySet

from apps.orders.models import Order


class OrderQueries:

    @staticmethod
    @database_sync_to_async
    def get_orders(restaurant_id: int) -> QuerySet:
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
