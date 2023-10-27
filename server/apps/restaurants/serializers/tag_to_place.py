from apps.core.serializers import BaseModelSerializer
from apps.restaurants.models import TagToPlace


class TagToProjectSerializer(BaseModelSerializer):
    class Meta:
        model = TagToPlace
        fields = (
            "id",
            "name",
        )
