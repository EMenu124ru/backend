from apps.core.serializers import BaseSerializer, serializers
from apps.orders.models import Dish, DishImage


class DishImageSerializer(BaseSerializer):
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
