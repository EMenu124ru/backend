from typing import Optional

from apps.users.models import User

from ..queries import RestaurantQueries, UserQueries


class ConnectValidation:

    @staticmethod
    async def validate(user: User, restaurant_id: str) -> Optional[str]:
        if not user.is_authenticated:
            return "User isn't authenticated"
        if (await UserQueries.is_client(user)):
            return "User isn't employee"
        if not (await UserQueries.check_role_employee_connect(user)):
            return "Employee has wrong role"
        if isinstance(restaurant_id, str) and not restaurant_id.isdigit():
            return "Enter right primary key of restaurant"
        restaurant_id = int(restaurant_id)
        if not (await RestaurantQueries.check_exists(restaurant_id)):
            return "Restaurant doesn't exists"
        if not (await RestaurantQueries.check_employee_consists(user, restaurant_id)):
            return "Employee isn't member of restaurant"
