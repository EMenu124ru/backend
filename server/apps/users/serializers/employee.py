from collections import OrderedDict

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
    email = serializers.CharField(source="user.email")
    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
        allow_null=True,
    )
    image = ObjectFileSerializer()

    class Errors:
        CANT_CHANGE = "Данное поле нельзя изменять"

    class Meta:
        model = Employee
        fields = (
            'id',
            'first_name',
            'last_name',
            'surname',
            'role',
            'phone_number',
            'date_of_birth',
            'address',
            'restaurant',
            'education',
            'place_of_birth',
            'citizenship',
            'personnel_number',
            'medical_checkup',
            'employment_contract',
            'work_experience',
            'image',
            'email',
        )
        read_only_fields = (
            'image',
            'restaurant',
        )

    def validate_restaurant(self, restaurant):
        if self.instance.restaurant != restaurant:
            raise serializers.ValidationError(self.Errors.CANT_CHANGE)
        return restaurant

    def validate_image(self, image):
        if self.instance.image != image:
            raise serializers.ValidationError(self.Errors.CANT_CHANGE)
        return image

    def update(self, instance: Employee, validated_data: OrderedDict) -> Employee:
        if "user" in validated_data:
            user_fields = validated_data.pop("user")
            instance.user.first_name = (
                user_fields.get("first_name", instance.user.first_name)
            )
            instance.user.last_name = (
                user_fields.get("last_name", instance.user.last_name)
            )
            instance.user.surname = (
                user_fields.get("surname", instance.user.surname)
            )
            instance.user.phone_number = (
                user_fields.get("phone_number", instance.user.phone_number)
            )
            instance.user.date_of_birth = (
                user_fields.get("date_of_birth", instance.user.date_of_birth)
            )
            instance.user.address = (
                user_fields.get("address", instance.user.address)
            )
            instance.user.email = (
                user_fields.get("email", instance.user.email)
            )
            instance.user.save()
        return super().update(instance, validated_data)

    def to_representation(self, instance: Employee):
        data = super().to_representation(instance)
        data["status"] = instance.get_status()
        return data
