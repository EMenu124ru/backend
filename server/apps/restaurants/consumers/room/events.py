class RestaurantEventsMixin:

    async def list_orders(self, event: dict) -> None:
        await self.send_event_response(event)
