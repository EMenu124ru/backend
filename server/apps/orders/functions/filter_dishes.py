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
    computed_ingredients = {}
    available_dishes = []
    for dish in dishes:
        is_available = True
        ingredients = dish.ingredients.all()
        ingredient_ids = []
        for ingredient in ingredients:
            if ingredient.id in computed_ingredients:
                if not computed_ingredients[ingredient.id]:
                    is_available = False
            else:
                computed_ingredients[ingredient.id] = True
                ingredient_ids.append(ingredient.id)
        if ingredient_ids:
            stop_list = StopList.objects.filter(
                ingredient_id__in=ingredient_ids,
                restaurant_id=restaurant_id,
            )
            if stop_list.exists():
                is_available = False
                for item in stop_list:
                    computed_ingredients[item.ingredient.id] = False
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
