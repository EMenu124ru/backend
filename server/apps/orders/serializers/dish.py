from collections import OrderedDict

from apps.core.serializers import BaseModelSerializer, serializers
from apps.orders.models import (
    Category,
    Dish,
    DishImage,
    Ingredient,
)

from .category import CategorySerializer


class IngredientSerializer(BaseModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            "id",
            "name",
        )


class DishImageSerializer(BaseModelSerializer):
    dish = serializers.PrimaryKeyRelatedField(
        queryset=Dish.objects.all(),
        write_only=True,
    )

    class Meta:
        model = DishImage
        fields = (
            "id",
            "dish",
            "image",
        )


class DishSerializer(BaseModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Dish
        fields = (
            "id",
            "category",
            "name",
            "description",
            "short_description",
            "price",
            "compound",
            "weight",
        )

    def to_representation(self, instance: Dish) -> OrderedDict:
        data = super().to_representation(instance)
        new_info = {
            "images": DishImageSerializer(instance.images.all(), many=True).data,
            "category": CategorySerializer(instance=instance.category).data,
        }
        data.update(new_info)
        return data
