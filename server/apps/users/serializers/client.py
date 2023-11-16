from rest_framework_simplejwt.tokens import RefreshToken

from apps.core.serializers import BaseModelSerializer, serializers
from apps.users.models import Client, User


class ClientAuthSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    class Errors:
        CLIENT_ALREADY_EXISTS = "Клиента с таким номером телефона не найдено"
        WRONG_PASSWORD = 'Не верный пароль'

    def to_representation(self, data):
        client = Client.objects.filter(
            phone_number=data['phone_number'],
        ).first()
        refresh = RefreshToken.for_user(client.user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

    def validate_phone_number(self, phone_number: str) -> str:
        if Client.objects.filter(phone_number=phone_number).exists():
            return phone_number
        raise serializers.ValidationError(self.Errors.CLIENT_ALREADY_EXISTS)

    def validate(self, attrs):
        if (
            client :=
            Client.objects.filter(
                phone_number=attrs['phone_number'],
            ).first()
        ):
            if not client.user.check_password(attrs['password']):
                raise serializers.ValidationError(self.Errors.WRONG_PASSWORD)
        return attrs


class ClientSerializer(BaseModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    surname = serializers.CharField(source="user.surname", default="")
    password = serializers.CharField(source="user.password", write_only=True)
    bonuses = serializers.IntegerField(default=0)

    class Errors:
        CANT_CHANGE_BONUSES = "Пользователь не может изменять количество бонусов"

    class Meta:
        model = Client
        fields = (
            'id',
            'bonuses',
            'phone_number',
            'first_name',
            'last_name',
            'surname',
            'password',
        )

    def create(self, validated_data) -> Client:
        user_fields = validated_data['user']
        username = (
            f"{user_fields['first_name']}_{user_fields['last_name']}"
            f"_{user_fields['surname']}_{validated_data['phone_number']}"
        )
        user = User.objects.create(
            username=username,
            first_name=user_fields['first_name'],
            last_name=user_fields['last_name'],
            surname=user_fields['surname'],
        )
        user.set_password(user_fields['password'])
        user.save()
        client = Client.objects.create(
            user=user,
            bonuses=validated_data['bonuses'],
            phone_number=validated_data['phone_number'],
        )
        return client

    def update(self, instance, validated_data) -> Client:
        if "user" in validated_data:
            user_fields = validated_data["user"]
            instance.user.first_name = (
                user_fields.get("first_name", instance.user.first_name)
            )
            instance.user.last_name = (
                user_fields.get("last_name", instance.user.last_name)
            )
            instance.user.surname = (
                user_fields.get("surname", instance.user.surname)
            )
            if "password" in validated_data["user"]:
                instance.user.set_password(
                    user_fields.pop("password")
                )
            instance.user.save()
        instance.phone_number = (
            validated_data.get("phone_number", instance.phone_number)
        )
        if "bonuses" in validated_data:
            raise serializers.ValidationError(self.Errors.CANT_CHANGE_BONUSES)
        instance.save()
        return instance
