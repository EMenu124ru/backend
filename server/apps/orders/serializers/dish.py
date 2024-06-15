from collections import OrderedDict

from apps.core.serializers import (
    BaseModelSerializer,
    ObjectFileSerializer,
    serializers,
)
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
    image = ObjectFileSerializer()

    class Meta:
        model = DishImage
        fields = (
            "id",
            "dish",
            "image",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        image = data["image"]
        data["image"] = image["file"]
        data["image_name"] = image["filename"]
        return data


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
            "weight",
        )

    def to_representation(self, instance: Dish) -> OrderedDict:
        data = super().to_representation(instance)
        images = instance.images.order_by("id")
        ingredients = instance.ingredients.order_by("id")
        compound = ", ".join([ingredient.name for ingredient in ingredients]) if ingredients else ""
        new_info = {
            "compound": compound,
            "images": DishImageSerializer(images, many=True).data,
            "category": CategorySerializer(instance=instance.category).data,
        }
        data.update(new_info)
        return data
