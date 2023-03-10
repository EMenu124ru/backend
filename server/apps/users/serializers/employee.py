from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
