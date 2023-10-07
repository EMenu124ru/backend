class RestaurantEventsMixin:

    async def employee_orders_retrieve(self, event: dict) -> None:
        await self.send_event_response(event)

    async def create_order(self, event: dict) -> None:
        await self.send_event_response(event)

    async def create_order_user(self, event: dict) -> None:
        await self.send_event_response(event)

    async def edit_order(self, event: dict) -> None:
        await self.send_event_response(event)

    async def edit_order_user(self, event: dict) -> None:
        await self.send_event_response(event)
