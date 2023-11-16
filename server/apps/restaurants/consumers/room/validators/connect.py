from typing import Final, Optional

from apps.users.models import User

from ..queries import RestaurantQueries, UserQueries


class ConnectValidation:

    class ConnectError:
        ISNT_AUTHENTICATED: Final[str] = "User isn't authenticated"
        ISNT_EMPLOYEE: Final[str] = "User isn't employee"
        WRONG_ROLE: Final[str] = "Employee has wrong role"
        WRONG_RESTAURANT_PK: Final[str] = "Enter right primary key of restaurant"
        RESTAURANT_NOT_EXISTS: Final[str] = "Restaurant doesn't exists"
        EMPLOYEE_ISNT_MEMBER: Final[str] = "Employee isn't member of restaurant"

    @staticmethod
    async def validate(user: User, restaurant_id: str) -> Optional[str]:
        if not user.is_authenticated:
            return ConnectValidation.ConnectError.ISNT_AUTHENTICATED
        if (await UserQueries.is_client(user)):
            return ConnectValidation.ConnectError.ISNT_EMPLOYEE
        if not (await UserQueries.check_role_employee_connect(user)):
            return ConnectValidation.ConnectError.WRONG_ROLE
        if isinstance(restaurant_id, str) and not restaurant_id.isdigit():
            return ConnectValidation.ConnectError.WRONG_RESTAURANT_PK
        restaurant_id = int(restaurant_id)
        if not (await RestaurantQueries.check_exists(restaurant_id)):
            return ConnectValidation.ConnectError.RESTAURANT_NOT_EXISTS
        if not (await RestaurantQueries.check_employee_consists(user, restaurant_id)):
            return ConnectValidation.ConnectError.EMPLOYEE_ISNT_MEMBER
