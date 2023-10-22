from apps.core.serializers import BaseModelSerializer
from apps.restaurants.models import Place


class PlaceSerializer(BaseModelSerializer):
    class Meta:
        model = Place
        fields = (
            "id",
            "place",
        )
