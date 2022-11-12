from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from . import models


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


class ClientAuthSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def to_representation(self, data):
        client = models.Client.objects.filter(
            phone_number=data['phone_number'],
        ).first()
        refresh = RefreshToken.for_user(client.user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

    def validate_phone_number(self, phone_number: str) -> str:
        if models.Client.objects.filter(phone_number=phone_number).exists():
            return phone_number
        raise serializers.ValidationError(
            "Клиента с таким номером телефона не найдено",
        )

    def validate(self, attrs):
        if (
            client :=
            models.Client.objects.filter(
                phone_number=attrs['phone_number'],
            ).first()
        ):
            if not client.user.check_password(attrs['password']):
                raise serializers.ValidationError(
                    'Не верный пароль',
                )
        return attrs


class ClientSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    password = serializers.CharField(source="user.password", write_only=True)
    bonuses = serializers.IntegerField(default=0)

    class Meta:
        model = models.Client
        fields = (
            'id',
            'bonuses',
            'phone_number',
            'first_name',
            'last_name',
            'password',
        )

    def create(self, validated_data) -> models.Client:
        user_fields = validated_data['user']
        username = (
            f"{user_fields['first_name']}_{user_fields['last_name']}"
            f"_{validated_data['phone_number']}"
        )
        user = models.User.objects.create(
            username=username,
            first_name=user_fields['first_name'],
            last_name=user_fields['last_name'],
        )
        user.set_password(user_fields['password'])
        user.save()
        client = models.Client.objects.create(
            user=user,
            bonuses=validated_data['bonuses'],
            phone_number=validated_data['phone_number'],
        )
        return client

    def update(self, instance, validated_data) -> models.Client:
        if "user" in validated_data:
            user_fields = validated_data["user"]
            instance.user.first_name = (
                user_fields.get("first_name", instance.user.first_name)
            )
            instance.user.last_name = (
                user_fields.get("last_name", instance.user.last_name)
            )
            if "password" in validated_data["user"]:
                instance.user.set_password(
                    user_fields.pop("password")
                )
            instance.user.save()
        instance.phone_number = (
            validated_data.get("phone_number", instance.phone_number)
        )
        instance.bonuses = (
            validated_data.get("bonuses", instance.bonuses)
        )
        instance.save()
        return instance
