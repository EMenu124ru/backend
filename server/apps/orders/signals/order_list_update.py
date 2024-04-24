from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.orders.functions import get_restaurant_id, update_order_list
from apps.orders.models import Order, OrderAndDish


@receiver(post_save, sender=Order)
def order_update_order_list(instance: Order, created: bool, **kwargs) -> None:
    if created:
        restaurant_id = get_restaurant_id(instance)
        update_order_list(restaurant_id, [instance])


@receiver(post_save, sender=OrderAndDish)
def order_and_dish_update_order_list(instance: OrderAndDish, created: bool, **kwargs) -> None:
    if created:
        restaurant_id = get_restaurant_id(instance.order)
        update_order_list(restaurant_id, [instance.order])
