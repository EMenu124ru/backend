from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from apps.orders.constants import CacheActions
from apps.orders.functions import get_or_create_cache_dishes
from apps.orders.models import StopList
from apps.orders.tasks import send_notification
from apps.users.models import Employee


def iterate_by_ingredients(stop_list):
    filter_params = {
        "user__employee__role": Employee.Roles.WAITER,
    }
    for dish in stop_list.ingredient.dishes.all():
        restaurant_id = stop_list.restaurant.id
        ingredient_name = stop_list.ingredient.name
        title = "Изменение стоп-листа"
        body = f"Ингредиент {ingredient_name} {'добавлен в стоп-лист' if stop_list.id else 'удален из стоп-листа'}"

        filter_params["user__employee__restaurant_id"] = restaurant_id

        send_notification.delay(filter_params, title, body)
        get_or_create_cache_dishes(
            CacheActions.CREATE,
            dish.category,
            restaurant_id,
        )


@receiver([post_save, post_delete], sender=StopList)
def update_stop_list_cache(instance, **kwargs) -> None:
    iterate_by_ingredients(instance)
