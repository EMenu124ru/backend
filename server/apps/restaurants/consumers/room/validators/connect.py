from typing import Final, Optional

from channels.layers import get_channel_layer
from django.core.cache import cache

from apps.users.models import User

from ..queries import RestaurantQueries, UserQueries


class ConnectValidation:

    class ConnectError:
        ISNT_AUTHENTICATED: Final[str] = "Пользователь не авторизирован"
        ISNT_EMPLOYEE: Final[str] = "Пользователь не является сотрудником"
        WRONG_ROLE: Final[str] = "Сотрудник не имеет права к подключению"
        WRONG_RESTAURANT_PK: Final[str] = "Введен не верный идентификатор ресторана"
        RESTAURANT_NOT_EXISTS: Final[str] = "Данного ресторана не существует"
        EMPLOYEE_ISNT_MEMBER: Final[str] = "Вы являетесь сотрудником другого ресторана"

    @staticmethod
    async def validate(user: User, restaurant_id: str, cache_key: str) -> Optional[str]:
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

        if item := await cache.aget(cache_key):
            await get_channel_layer().send(
                item,
                {
                    "type": "websocket.disconnect",
                    "code": 1000,
                },
            )
