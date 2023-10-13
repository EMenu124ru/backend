from django.core.exceptions import ValidationError as ValidationErrorDjango
from rest_framework.exceptions import ValidationError

from apps.core.services import get_errors

from .constants import Events
from .queries import OrderQueries
from .services import OrderAndDishService, OrderService


class RestaurantActionsMixin:

    async def employee_orders_list(self) -> None:
        messages = await OrderQueries.get_orders_by_restaurant(self.restaurant_id)
        body = {"orders": await OrderService.get_orders_list(messages)}
        await self.response_to_user(Events.LIST_ORDERS, body)

    async def create_order(self, body: dict) -> None:
        try:
            order_body = {
                "order": await OrderService.create_order(body, self.user.employee),
            }
        except (ValidationError, ValidationErrorDjango) as ex:
            errors = get_errors(ex.detail)
            error_message = "\n".join(map(str, set(errors)))
            await self.send_error(error_message)
        else:
            await self.response_to_group(Events.NEW_ORDER, order_body)

    async def edit_order(self, body: dict) -> None:
        try:
            order = await OrderQueries.get_order(body["id"])
            dishes = body.pop("dishes", [])
            await OrderAndDishService.edit_dishes(dishes, order.id, self.user)
            edited_order = await OrderService.edit_order(body, order, self.user)
            body = {"order": edited_order}
        except (ValidationError, ValidationErrorDjango) as ex:
            errors = get_errors(ex.detail)
            error_message = "\n".join(map(str, set(errors)))
            await self.send_error(error_message)
        else:
            await self.response_to_group(Events.ORDER_CHANGED, body)
