from rest_framework import serializers

from apps.users.models import Client

from . import models


class ReviewSerializer(serializers.ModelSerializer):

    client = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
    )

    class Meta:
        model = models.Review
        fields = (
            "id",
            "review",
            "mark",
            "client",
        )
