from apps.core.serializers import BaseModelSerializer, serializers
from apps.orders.models import Dish, DishImage


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
