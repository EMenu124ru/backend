from apps.core.serializers import BaseModelSerializer
from apps.restaurants.models import Restaurant


class RestaurantSerializer(BaseModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
            "id",
            "address",
        )
