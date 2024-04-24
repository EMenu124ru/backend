from collections import Counter

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.orders.models import Order, OrderAndDish

ORDER_AND_DISH_STATUS_WEIGHTS = {
    OrderAndDish.Statuses.WAITING_FOR_COOKING: 0,
    OrderAndDish.Statuses.COOKING: 1,
    OrderAndDish.Statuses.DONE: 2,
    OrderAndDish.Statuses.DELIVERED: 3,
}
CHECKED_STATUSES = [
    OrderAndDish.Statuses.WAITING_FOR_COOKING,
    OrderAndDish.Statuses.COOKING,
    OrderAndDish.Statuses.DELIVERED,
    OrderAndDish.Statuses.DONE,
]


@receiver(post_save, sender=OrderAndDish)
def change_order_status_based_on_dishes(instance: OrderAndDish, **kwargs) -> None:
    order = instance.order
    if instance.status == OrderAndDish.Statuses.CANCELED:
        instance.delete()
    if order.status == Order.Statuses.DELAYED:
        return
    order_status = Order.Statuses.WAITING_FOR_COOKING
    dishes = order.dishes.filter(status__in=CHECKED_STATUSES).all()
    count_dishes = dishes.count()
    if not count_dishes:
        order.status = order_status
        order.save()
        return
    counter = Counter(dishes.values_list("status", flat=True))
    min_status = min(counter, key=lambda obj: ORDER_AND_DISH_STATUS_WEIGHTS[obj])
    if min_status == OrderAndDish.Statuses.WAITING_FOR_COOKING:
        order_status = Order.Statuses.WAITING_FOR_COOKING
    elif min_status == OrderAndDish.Statuses.COOKING:
        order_status = Order.Statuses.COOKING
        if OrderAndDish.Statuses.DONE in counter:
            order_status = Order.Statuses.WAITING_FOR_DELIVERY
    elif min_status == OrderAndDish.Statuses.DONE:
        order_status = Order.Statuses.WAITING_FOR_DELIVERY
    elif min_status == OrderAndDish.Statuses.DELIVERED:
        order_status = Order.Statuses.DELIVERED
    if instance.order.status != order_status:
        instance.order.status = order_status
        instance.order.save()
