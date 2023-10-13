from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.core.serializers import BaseModelSerializer
from apps.restaurants.models import Restaurant
from apps.users.models import Employee


class EmployeeAuthSerializer(TokenObtainPairSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if self.user.is_client:
            raise serializers.ValidationError(
                'Пользователь не является сотрудником',
            )
        return {
            'access': validated_data['access'],
            'refresh': validated_data['refresh'],
        }


class EmployeeSerializer(BaseModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
        source="restaurant.id",
        allow_null=True,
    )

    class Meta:
        model = Employee
        fields = (
            'id',
            'first_name',
            'last_name',
            'role',
            'restaurant',
        )
