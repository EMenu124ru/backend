from collections import OrderedDict

from apps.core.serializers import BaseSerializer, serializers
from apps.orders.models import Dish, Category
from .category import CategorySerializer
from .dish_image import DishImageSerializer


class DishSerializer(BaseSerializer):
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
