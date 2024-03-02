from apps.core.serializers import BaseModelSerializer, ObjectFileSerializer
from apps.orders.models import Category


class CategorySerializer(BaseModelSerializer):
    icon = ObjectFileSerializer()

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "icon",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        icon = data["icon"]
        data["icon"] = icon["file"]
        data["icon_name"] = icon["filename"]
        return data
