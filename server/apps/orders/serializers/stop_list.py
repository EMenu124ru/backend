from apps.core.serializers import BaseModelSerializer, serializers
from apps.orders.models import Dish, StopList
from apps.restaurants.models import Restaurant


class StopListSerializer(BaseModelSerializer):
    dish = serializers.PrimaryKeyRelatedField(
        queryset=Dish.objects.all(),
    )
    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
        allow_null=True,
        required=False,
    )

    class Errors:
        STOP_LIST_WITHOUT_DISHES = "Нельзя создать стоп лист без блюд"

    class Meta:
        model = StopList
        fields = (
            "id",
            "dish",
            "restaurant",
        )

    def validate_dishes(self, dishes) -> list:
        if not dishes:
            raise serializers.ValidationError(self.Errors.STOP_LIST_WITHOUT_DISHES)
        return dishes
