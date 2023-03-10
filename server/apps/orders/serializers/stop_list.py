from apps.core.serializers import BaseSerializer, serializers
from apps.restaurants.models import Restaurant

from apps.orders.models import StopList, Dish


class StopListSerializer(BaseSerializer):
    dish = serializers.PrimaryKeyRelatedField(
        queryset=Dish.objects.all(),
    )
    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = StopList
        fields = (
            "id",
            "dish",
            "restaurant",
        )

    def validate_dishes(self, dishes) -> list:
        if not dishes:
            raise serializers.ValidationError(
                "Нельзя создать стоп лист без блюд",
            )
        return dishes
