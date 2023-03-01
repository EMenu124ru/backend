from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.orders.models import OrderAndDishes, Order


@receiver(post_save, sender=OrderAndDishes)
def change_order_status_based_on_dishes(instance, created, **kwargs) -> None:
    dishes_from_same_order = OrderAndDishes.objects.filter(
        order_id=instance.order.id,
    )
    if dishes_from_same_order.filter(status=OrderAndDishes.Statuses.COOKING).exists():
        instance.order.status = Order.Statuses.COOKING
    is_all_ready = True
    if  not dishes_from_same_order.filter(status=OrderAndDishes.Statuses.DONE).exists():
        is_all_ready = False
    if is_all_ready:
        instance.order.status = Order.Statuses.WAITING_FOR_DELIVERY
    instance.order.save()
