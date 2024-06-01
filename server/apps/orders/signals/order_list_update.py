from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.core.tasks import send_notification
from apps.orders.constants import NotificationText
from apps.orders.functions import (
    change_reservation_status,
    get_restaurant_id,
    update_order_list_in_group,
)
from apps.orders.models import Order
from apps.users.models import Employee


@receiver(post_save, sender=Order)
def order_update_order_list(instance: Order, created: bool, update_fields: frozenset, **kwargs) -> None:
    restaurant_id = get_restaurant_id(instance)
    filter_params = {
        "user__employee__restaurant_id": restaurant_id,
    }

    changed_reservation_statuses = [Order.Statuses.CANCELED, Order.Statuses.FINISHED]

    update_order_list_in_group(restaurant_id)
    if created:
        filter_params["user__employee__role__in"] = [Employee.Roles.CHEF, Employee.Roles.SOUS_CHEF]
        body = NotificationText.ORDER_NEW.body
        send_notification.delay(filter_params, NotificationText.ORDER_NEW.title, body.format(instance.id))
    else:
        if "status" in update_fields:
            filter_params["user__employee__role"] = Employee.Roles.WAITER
            filter_params["user__employee__id"] = instance.employee.id
            body = NotificationText.ORDER_UPDATED.body
            body = body.format(instance.id, instance.status)
            send_notification.delay(filter_params, NotificationText.ORDER_UPDATED.title, body)

            if instance.status in changed_reservation_statuses:
                change_reservation_status(instance.reservation)
