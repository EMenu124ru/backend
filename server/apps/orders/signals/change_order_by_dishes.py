from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.orders.functions import order_change_price, order_change_status
from apps.orders.models import Order, OrderAndDish


@receiver(post_save, sender=OrderAndDish)
def change_order_based_on_dishes(instance: OrderAndDish, **kwargs) -> None:
    order = instance.order
    if instance.status == OrderAndDish.Statuses.CANCELED:
        instance.delete()
    if order.status == Order.Statuses.DELAYED:
        return

    order_status = order_change_status(order)
    if order.status != order_status:
        order.status = order_status
        order.save()

    order_price = order_change_price(order)
    if order.price != order_price:
        order.price = order_price
        order.save()
