from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404

from apps.orders.models import OrderAndDish
from apps.orders.serializers import OrderAndDishSerializer
from apps.users.models import User


class OrderAndDishService:

    @staticmethod
    @database_sync_to_async
    def edit_dishes(dishes: list, order_id: int, user: User) -> None:
        for item in dishes:
            serializer = None
            item["order"] = order_id
            if item.get("id"):
                obj = get_object_or_404(OrderAndDish, pk=item["id"])
                serializer = OrderAndDishSerializer(
                    obj,
                    data=item,
                    partial=True,
                    context={'user': user},
                )
            else:
                serializer = OrderAndDishSerializer(
                    data=item,
                    context={'user': user},
                )
            serializer.is_valid(raise_exception=True)
            serializer.save()

    @staticmethod
    @database_sync_to_async
    def check_can_edit_order(body: dict) -> bool:
        return (
            len(body) == 2
            and "id" in body and "dishes" in body and
            all(["id" in dish for dish in body["dishes"]])
        )
