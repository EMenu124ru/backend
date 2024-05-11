from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.orders.models import OrderAndDish

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
def change_order_price_based_on_dishes(instance: OrderAndDish, **kwargs) -> None:
    order = instance.order
    new_price = 0
    for dish in order.dishes.filter(~Q(status=OrderAndDish.Statuses.CANCELED)):
        new_price += dish.dish.price
    order.price = new_price
    order.save()
