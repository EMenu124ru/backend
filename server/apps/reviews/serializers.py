from typing import OrderedDict

from apps.core.serializers import BaseSerializer, serializers
from apps.orders.models import Dish
from apps.restaurants.models import Restaurant
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

    dish = serializers.PrimaryKeyRelatedField(
        queryset=Dish.objects.all(),
        required=False,
        write_only=True,
    )
    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
        required=False,
        write_only=True,
    )

    class Meta:
        model = models.Review
        fields = (
            "id",
            "mark",
            "review",
            "dish",
            "restaurant",
        )

    def create(self, validated_data: OrderedDict) -> models.Review:
        if (
            validated_data.get("dish", None) is None and
            validated_data.get("restaurant", None) is None
        ):
            raise serializers.ValidationError(
                "Нет объекта для присвоения ему отзыва",
            )
        object_for_add = (
            validated_data.pop("dish")
            if "dish" in validated_data
            else validated_data.pop("restaurant")
        )
        review = super().create(validated_data)
        object_for_add.reviews.add(review)
        return review

    def to_representation(self, instance: models.Review) -> OrderedDict:
        data = super().to_representation(instance)
        new_info = {
            "images": ReviewImagesSerializer(instance.images.all(), many=True).data,
            "client": ClientSerializer(instance=instance.client).data,
        }
        data.update(new_info)
        return data
