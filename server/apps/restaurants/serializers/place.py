from apps.core.serializers import BaseModelSerializer
from apps.restaurants.models import Place, TagToPlace


class TagToPlaceSerializer(BaseModelSerializer):
    class Meta:
        model = TagToPlace
        fields = (
            "id",
            "name",
        )


class PlaceSerializer(BaseModelSerializer):
    class Meta:
        model = Place
        fields = (
            "id",
            "place",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["tags"] = TagToPlaceSerializer(instance.tags.all(), many=True).data
        return data
