from .constants import Events
from .queries import OrderQueries
from .services import OrderService


class RestaurantActionsMixin:

    async def employee_orders_list(self) -> None:
        messages = await OrderQueries.get_orders(self.restaurant_id)
        body = {"orders": await OrderService.get_orders_list(messages)}
        await self.response_to_user(Events.EMPLOYEE_ORDERS_RETRIEVE, body)
