from channels.exceptions import DenyConnection
from django.core.cache import cache

from apps.core.consumer import BaseConsumer

from .actions import RestaurantActionsMixin
from .constants import Actions
from .events import RestaurantEventsMixin
from .validators import ConnectValidation


class RestaurantConsumer(
    BaseConsumer,
    RestaurantActionsMixin,
    RestaurantEventsMixin,
):

    ACTION_MAP = {
        Actions.EMPLOYEE_ORDERS_LIST: RestaurantActionsMixin.employee_orders_list,
        Actions.CREATE_ORDER: RestaurantActionsMixin.create_order,
        Actions.EDIT_ORDER: RestaurantActionsMixin.edit_order,
    }

    async def connect(self):
        self.restaurant_id = self.scope["url_route"]["kwargs"]["restaurant_id"]
        self.group_name = f"restaurant_{self.restaurant_id}"
        self.user = self.scope["user"]
        self.cache_key = f"user__{self.user.id}__{self.restaurant_id}"
        await self.accept()
        if error := await ConnectValidation.validate(
            self.user,
            self.restaurant_id,
            self.cache_key,
        ):
            await self.send_error(error)
            raise DenyConnection()

        self.restaurant_id = int(self.restaurant_id)
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

        await cache.aset(self.cache_key, self.channel_name, timeout=24*60*60)
        await RestaurantActionsMixin.employee_orders_list(self)

    async def disconnect(self, close_code):
        await cache.adelete_many([self.cache_key])
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )
        await self.close()
