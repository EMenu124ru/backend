from apps.core.serializers import BaseModelSerializer
from apps.orders.models import Category


class CategorySerializer(BaseModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )
