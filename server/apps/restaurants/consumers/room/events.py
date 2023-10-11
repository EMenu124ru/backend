class RestaurantEventsMixin:

    async def list_orders(self, event: dict) -> None:
        await self.send_event_response(event)

    async def new_order(self, event: dict) -> None:
        await self.send_event_response(event)

    async def order_changed(self, event: dict) -> None:
        await self.send_event_response(event)
