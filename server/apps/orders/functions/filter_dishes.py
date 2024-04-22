import enum

from django.core.cache import cache
from django.db.models import QuerySet

from apps.orders.models import (
    Category,
    Dish,
    StopList,
)

CACHE_DISHES_KEY = "dishes_category_{}_restaurant_{}"
CACHE_TIMEOUT = 60 * 60 * 24


class CacheActions(enum.Enum):
    GET = 0
    CREATE = 1


def get_available_dishes(dishes: QuerySet, restaurant_id: int) -> QuerySet:
    available_dishes = []
    restaurant_stop_list = StopList.objects.filter(restaurant_id=restaurant_id)
    for dish in dishes:
        is_available = True
        ingredients_ids = dish.ingredients.values_list('id', flat=True)
        is_available = not restaurant_stop_list.filter(
            ingredient_id__in=ingredients_ids,
        ).exists()
        if is_available:
            available_dishes.append(dish.id)
    return Dish.objects.filter(id__in=available_dishes)


def get_or_create_cache_dishes(
    action: str,
    category: Category,
    restaurant_id: int,
) -> Dish:
    key = CACHE_DISHES_KEY.format(category.id, restaurant_id)
    cached_dishes = cache.get(key)
    if action == CacheActions.GET and cached_dishes:
        return cached_dishes
    queryset = category.dishes.all()
    dishes = get_available_dishes(queryset, restaurant_id)
    cache.set(key, dishes, CACHE_TIMEOUT)
    return dishes
