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
