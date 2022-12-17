from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.orders.models import OrderAndDishes


@receiver(post_save, sender=OrderAndDishes)
def change_order_status_based_on_dishes(instance, created, **kwargs) -> None:
    print("order and dishes created")

