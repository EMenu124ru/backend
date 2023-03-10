from apps.core.serializers import BaseSerializer, serializers
from apps.reviews.models import Review, ReviewImage


class ReviewImageSerializer(BaseSerializer):
    review = serializers.PrimaryKeyRelatedField(
        queryset=Review.objects.all(),
        write_only=True,
    )

    class Meta:
        model = ReviewImage
        fields = (
            "id",
            "image",
            "review",
        )
