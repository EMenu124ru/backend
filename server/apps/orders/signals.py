from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.orders.models import OrderAndDishes, Order


@receiver(post_save, sender=OrderAndDishes)
def change_order_status_based_on_dishes(instance, created, **kwargs) -> None:
    if created:
        print("created")
        return
    print("is it working??")
    dishes_from_same_order = OrderAndDishes.objects.filter(
        order=instance.order,
    )
    for dish in dishes_from_same_order:
        if dish.status == OrderAndDishes.Statuses.COOKING:
            print("changing order status to cooking")
            instance.order.status = Order.Statuses.COOKING
            return
    is_all_ready = True
    for dish in dishes_from_same_order:
        if dish.status != OrderAndDishes.Statuses.DONE:
            is_all_ready = False
            break
    if is_all_ready:
        print("changing order status to waiting for delivery")
        instance.order.status = Order.Statuses.WAITING_FOR_DELIVERY
