from channels.db import database_sync_to_async
from django.db.models import QuerySet

from apps.restaurants.models import Restaurant


class RestaurantQueries:

    @staticmethod
    @database_sync_to_async
    def check_exists(restaurant_id: int) -> bool:
        return Restaurant.objects.filter(id=restaurant_id).exists()
