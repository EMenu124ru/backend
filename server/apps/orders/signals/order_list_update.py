from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.orders.models import Order, OrderAndDish

ACCESS_STATUS = [
    Order.Statuses.WAITING_FOR_COOKING,
    Order.Statuses.COOKING,
    Order.Statuses.WAITING_FOR_DELIVERY,
    Order.Statuses.IN_PROCESS_DELIVERY,
]


def update_order_list(restaurant_id):
    from apps.restaurants.consumers.room import (
        Events,
        OrderQueries,
        OrderService,
    )

    group_name = f"restaurant_{restaurant_id}"
    orders = OrderQueries.get_orders_by_restaurant_sync(restaurant_id)
    body = {"orders": OrderService.get_orders_list_sync(orders)}
    async_to_sync(get_channel_layer().group_send)(
        group_name,
        {
            "type": Events.LIST_ORDERS,
            "body": body,
        },
    )


def get_restaurant_id(order: Order):
    employee = order.employee
    if employee and employee.restaurant_id:
        return employee.restaurant_id

    reservation = order.reservation
    if reservation and reservation.restaurant_id:
        return reservation.restaurant_id


@receiver(post_save, sender=Order)
def order_update_order_list(instance, **kwargs) -> None:
    restaurant_id = get_restaurant_id(instance)
    if restaurant_id:
        update_order_list(restaurant_id)


@receiver(post_save, sender=OrderAndDish)
def order_and_dish_update_order_list(instance, **kwargs) -> None:
    restaurant_id = get_restaurant_id(instance.order)
    if restaurant_id:
        update_order_list(restaurant_id)
