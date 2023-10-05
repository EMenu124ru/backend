from typing import Optional

from apps.users.models import User
from ..queries import RestaurantQueries


class ConnectValidation:

    @staticmethod
    async def validate(user: User, restaurant_id: str) -> Optional[str]:
        if user.is_client:
            return "User isn't employee"
        if isinstance(restaurant_id, str) and not restaurant_id.isdigit():
            return "Enter right primary key of restaurant"
        restaurant_id = int(restaurant_id)
        if not (await RestaurantQueries.check_exists(restaurant_id)):
            return "Restaurant doesn't exists"
        if user.employee.restaurant.id != restaurant_id:
            return "Employee isn't member of restaurant"
