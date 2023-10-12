from channels.db import database_sync_to_async

from apps.restaurants.models import Restaurant
from apps.users.models import User


class RestaurantQueries:

    @staticmethod
    @database_sync_to_async
    def check_exists(restaurant_id: int) -> bool:
        return Restaurant.objects.filter(id=restaurant_id).exists()

    @staticmethod
    @database_sync_to_async
    def check_employee_consists(user: User, restaurant_id: int) -> bool:
        return user.employee.restaurant.id == restaurant_id
