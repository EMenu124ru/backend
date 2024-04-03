from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.orders.functions import CacheActions, get_or_create_cache_dishes
from apps.orders.models import StopList


def iterate_by_ingredients(stop_list):
    for dish in stop_list.ingredient.dishes.all():
        get_or_create_cache_dishes(CacheActions.CREATE, dish.category, stop_list.restaurant.id)


@receiver([post_save, post_delete], sender=StopList)
def update_stop_list_cache(instance, **kwargs) -> None:
    iterate_by_ingredients(instance)
