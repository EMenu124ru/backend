from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.core.tasks import send_notification
from apps.orders.constants import CacheActions, NotificationText
from apps.orders.functions import get_or_create_cache_dishes
from apps.orders.models import StopList
from apps.users.models import Employee


def iterate_by_ingredients(stop_list: StopList) -> None:
    restaurant_id = stop_list.restaurant.id
    ingredient_name = stop_list.ingredient.name
    notification_type = NotificationText.STOP_LIST_ADD if stop_list.id else NotificationText.STOP_LIST_REMOVE
    body = notification_type.body.format(ingredient_name)

    filter_params = {
        "user__employee__restaurant_id": restaurant_id,
        "user__employee__role": Employee.Roles.WAITER,
    }

    send_notification.delay(filter_params, notification_type.title, body)
    for dish in stop_list.ingredient.dishes.all():
        get_or_create_cache_dishes(
            CacheActions.CREATE,
            dish.category,
            restaurant_id,
        )


@receiver([post_save, post_delete], sender=StopList)
def update_stop_list_cache(instance: StopList, **kwargs) -> None:
    iterate_by_ingredients(instance)
