from apps.core.serializers import BaseSerializer
from apps.orders.models import Category


class CategorySerializer(BaseSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )
