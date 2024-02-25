from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.orders.models import Order, OrderAndDish


@receiver(post_save, sender=OrderAndDish)
def change_order_status_based_on_dishes(instance, **kwargs) -> None:
    dishes_from_same_order = OrderAndDish.objects.filter(
        order_id=instance.order.id,
    )
    DONE_ALLOW_STATUSES = [
        OrderAndDish.Statuses.DONE,
        OrderAndDish.Statuses.CANCELED,
    ]
    if dishes_from_same_order.filter(status=OrderAndDish.Statuses.COOKING).exists():
        instance.order.status = Order.Statuses.COOKING
    is_all_ready = True
    if dishes_from_same_order.filter(~Q(status__in=DONE_ALLOW_STATUSES)).exists():
        is_all_ready = False
    if is_all_ready:
        instance.order.status = Order.Statuses.WAITING_FOR_DELIVERY
    instance.order.save()
