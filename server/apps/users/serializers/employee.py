from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.core.serializers import BaseModelSerializer
from apps.restaurants.models import Restaurant
from apps.users.models import Employee


class EmployeeAuthSerializer(TokenObtainPairSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Errors:
        USER_ISNT_EMPLOYEE = 'Пользователь не является сотрудником'

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if self.user.is_client:
            raise serializers.ValidationError(self.Errors.USER_ISNT_EMPLOYEE)
        return {
            'access': validated_data['access'],
            'refresh': validated_data['refresh'],
        }


class EmployeeSerializer(BaseModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    surname = serializers.CharField(source="user.surname")
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
            'surname',
            'role',
            'restaurant',
        )
