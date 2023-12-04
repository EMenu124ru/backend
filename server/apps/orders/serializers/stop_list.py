from typing import OrderedDict

from apps.core.serializers import BaseModelSerializer, serializers
from apps.orders.models import Ingredient, StopList
from apps.orders.serializers import DishSerializer
from apps.restaurants.models import Restaurant


class StopListSerializer(BaseModelSerializer):
    ingredient = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
    )
    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
    )

    class Errors:
        STOP_LIST_WITHOUT_INGREDIENT = "Нельзя создать стоп лист без ингредиента"

    class Meta:
        model = StopList
        fields = (
            "id",
            "ingredient",
            "restaurant",
            "created_at",
        )

    def validate_ingredient(self, ingredient) -> list:
        if not ingredient:
            raise serializers.ValidationError(self.Errors.STOP_LIST_WITHOUT_INGREDIENT)
        return ingredient

    def to_representation(self, instance: StopList) -> OrderedDict:
        data = super().to_representation(instance)
        new_info = {
            "dishes": DishSerializer(instance.ingredient.dishes.all(), many=True).data,
        }
        data.update(new_info)
        return data
