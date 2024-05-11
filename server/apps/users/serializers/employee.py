from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.core.serializers import BaseModelSerializer, ObjectFileSerializer
from apps.restaurants.models import Restaurant
from apps.users.models import Employee


class EmployeeAuthSerializer(TokenObtainPairSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Errors:
        USER_IS_NOT_EMPLOYEE = 'Пользователь не является сотрудником'

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if self.user.is_client:
            raise serializers.ValidationError(self.Errors.USER_IS_NOT_EMPLOYEE)
        return {
            'access': validated_data['access'],
            'refresh': validated_data['refresh'],
        }


class EmployeeSerializer(BaseModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    surname = serializers.CharField(source="user.surname")
    phone_number = serializers.CharField(source="user.phone_number")
    date_of_birth = serializers.DateField(source="user.date_of_birth")
    address = serializers.CharField(source="user.address")
    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
        source="restaurant.id",
        allow_null=True,
    )
    image = ObjectFileSerializer()

    class Meta:
        model = Employee
        fields = (
            'id',
            'first_name',
            'last_name',
            'surname',
            'phone_number',
            'date_of_birth',
            'address',
            'education',
            'place_of_birth',
            'citizenship',
            'personnel_number',
            'medical_checkup',
            'employment_contract',
            'work_experience',
            'role',
            'restaurant',
            'image',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["status"] = instance.get_status()
        return data
