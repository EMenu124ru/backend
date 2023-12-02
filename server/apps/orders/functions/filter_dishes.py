from django.db.models import QuerySet

from apps.orders.models import Dish, StopList


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
