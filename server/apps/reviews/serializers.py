from typing import OrderedDict

from apps.core.serializers import BaseSerializer, serializers
from apps.users.models import Client
from apps.users.serializers import ClientSerializer

from . import models


class ReviewImagesSerializer(BaseSerializer):

    review = serializers.PrimaryKeyRelatedField(
        queryset=models.Review.objects.all(),
        write_only=True,
    )

    class Meta:
        model = models.ReviewImages
        fields = (
            "id",
            "image",
            "review",
        )


class ReviewSerializer(BaseSerializer):

    client = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
    )

    class Meta:
        model = models.Review
        fields = (
            "id",
            "mark",
            "review",
            "client",
        )

    def to_representation(self, instance: models.Review) -> OrderedDict:
        data = super().to_representation(instance)
        new_info = {
            "images": ReviewImagesSerializer(instance.images.all(), many=True).data,
            "client": ClientSerializer(instance=instance.client).data,
        }
        data.update(new_info)
        return data
