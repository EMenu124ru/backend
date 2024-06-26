from apps.core.serializers import BaseModelSerializer
from apps.restaurants.models import Place, TagToPlace


class TagToPlaceSerializer(BaseModelSerializer):
    class Meta:
        model = TagToPlace
        fields = (
            "id",
            "name",
            "type",
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
        data["current_reservation_id"] = getattr(instance, "current_reservation", None)
        data["client_full_name"] = getattr(instance, "client_full_name", None)
        data["tags"] = TagToPlaceSerializer(instance.tags.all(), many=True).data
        return data
