from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.orders.models import Order, Reservation


@receiver(post_save, sender=Reservation)
def changes_by_reservation(instance: Reservation, created: bool, update_fields: frozenset, **kwargs) -> None:
    if not created:
        if update_fields and "status" in update_fields:
            mapping_statuses = {
                Reservation.Statuses.CANCELED: Order.Statuses.CANCELED,
                Reservation.Statuses.FINISHED: Order.Statuses.FINISHED,
            }
            if instance.status in mapping_statuses:
                instance.orders.update(status=mapping_statuses[instance.status])
