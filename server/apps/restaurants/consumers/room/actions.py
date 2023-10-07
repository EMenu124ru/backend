from .constants import Events
from .queries import OrderQueries
from .services import OrderService


class RestaurantActionsMixin:

    async def employee_orders_list(self) -> None:
        messages = await OrderQueries.get_orders_by_restaurant(self.restaurant_id)
        body = {"orders": await OrderService.get_orders_list(messages)}
        await self.response_to_user(Events.EMPLOYEE_ORDERS_RETRIEVE, body)
    
    async def create_order(self, body: dict) -> None:
        order = await OrderService.create_order(body, self.user.employee)
        body = {"order": order}
        await self.response_to_group(Events.CREATE_ORDER, body)
        await self.response_to_user(Events.CREATE_ORDER_USER, body)

    async def edit_order(self, body: dict) -> None:
        order = await OrderQueries.get_order(body["id"])
        update_order = OrderService.edit_order(body, order)
        body = {"order": update_order}
        await self.response_to_group(Events.EDIT_ORDER, body)
        await self.response_to_user(Events.EDIT_ORDER_USER, body)
