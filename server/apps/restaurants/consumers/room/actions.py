from django.core.exceptions import ValidationError as ValidationErrorDjango
from rest_framework.exceptions import ValidationError

from apps.core.utils import get_errors

from .constants import Errors, Events
from .queries import OrderQueries, UserQueries
from .services import OrderAndDishService, OrderService


class RestaurantActionsMixin:

    async def employee_orders_list(self) -> None:
        messages = await OrderQueries.get_orders_by_restaurant(self.restaurant_id)
        body = {"orders": await OrderService.get_orders_list(messages)}
        await self.response_to_user(Events.LIST_ORDERS, body)

    async def create_order(self, body: dict) -> None:
        if (await UserQueries.check_role_employee_cant_create_order(self.user)):
            await self.send_error(Errors.CANT_CREATE_ORDER)
        try:
            order_body = {
                "order": await OrderService.create_order(body, self.user.employee),
            }
        except (ValidationError, ValidationErrorDjango) as ex:
            error_message = get_errors(ex.detail)
            error_message_str = (
                f"{error_message[0]['field']} - {error_message[0]['message']}"
            )
            await self.send_error(error_message_str)
        else:
            await self.response_to_group(Events.NEW_ORDER, order_body)

    async def edit_order(self, body: dict) -> None:
        try:
            cant_edit = await UserQueries.check_role_employee_cant_edit_order(self.user)
            if cant_edit and not (await OrderAndDishService.check_can_edit_order(body)):
                await self.send_error(Errors.CANT_EDIT_ORDER)
            order = await OrderQueries.get_order(body["id"])
            dishes = body.pop("dishes", [])
            await OrderAndDishService.edit_dishes(dishes, order.id, self.user)
            edited_order = await OrderService.edit_order(body, order, self.user)
            body = {"order": edited_order}
        except (ValidationError, ValidationErrorDjango) as ex:
            error_message = get_errors(ex.detail)
            error_message_str = (
                f"{error_message[0]['field']} - {error_message[0]['message']}"
            )
            await self.send_error(error_message_str)
        else:
            await self.response_to_group(Events.ORDER_CHANGED, body)
