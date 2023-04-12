from apps.core.serializers import BaseModelSerializer
from apps.restaurants.models import Plan


class PlanSerializer(BaseModelSerializer):
    class Meta:
        model = Plan
        fields = (
            "id",
            "plan",
        )
