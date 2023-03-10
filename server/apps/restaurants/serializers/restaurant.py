from rest_framework import serializers

from apps.restaurants.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
            "id",
            "address",
        )
