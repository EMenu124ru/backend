class RestaurantEventsMixin:

    async def employee_orders_retrieve(self, event: dict) -> None:
        await self.send_event_response(event)
