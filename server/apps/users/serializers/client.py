from apps.core.serializers import BaseModelSerializer, serializers
from apps.core.utils import get_jwt_tokens
from apps.users.models import Client, User


class ClientAuthSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    class Errors:
        CLIENT_DONT_EXISTS = "Клиента с таким номером телефона не найдено"
        WRONG_PASSWORD = 'Не верный пароль'
        IS_NOT_ACTIVE = 'Пользователь не активен'

    def validate_phone_number(self, phone_number: str) -> str:
        if not Client.objects.filter(user__phone_number=phone_number).exists():
            raise serializers.ValidationError(self.Errors.CLIENT_DONT_EXISTS)
        return phone_number

    def validate(self, attrs):
        if (
            client :=
            Client.objects.filter(
                user__phone_number=attrs['phone_number'],
            ).first()
        ):
            if not client.user.is_active:
                raise serializers.ValidationError(self.Errors.IS_NOT_ACTIVE)
            if not client.user.check_password(attrs['password']):
                raise serializers.ValidationError(self.Errors.WRONG_PASSWORD)

        return attrs

    def to_representation(self, data):
        client = Client.objects.filter(
            user__phone_number=data['phone_number'],
        ).first()
        return get_jwt_tokens(client.user)


class ClientSerializer(BaseModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    surname = serializers.CharField(
        source="user.surname",
        required=False,
        allow_null=True,
        default="",
    )
    phone_number = serializers.CharField(source="user.phone_number")
    password = serializers.CharField(
        source="user.password",
        write_only=True,
        required=False,
        allow_null=True,
    )
    bonuses = serializers.IntegerField(default=0)

    class Errors:
        CANT_CHANGE_BONUSES = "Пользователь не может изменять количество бонусов"
        CLIENT_ALREADY_EXISTS = "Клиент с такими данными уже существует"

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
            f"_{user_fields['surname']}_{user_fields['phone_number']}"
        )

        user, created = User.objects.get_or_create(
            username=username,
            first_name=user_fields['first_name'],
            last_name=user_fields['last_name'],
            surname=user_fields['surname'],
            phone_number=user_fields['phone_number'],
        )
        if not created:
            raise serializers.ValidationError(self.Errors.CLIENT_ALREADY_EXISTS)

        if 'password' not in user_fields:
            user.set_password(username)
        else:
            user.set_password(user_fields['password'])
        user.save()

        client = Client.objects.create(
            user=user,
            bonuses=validated_data['bonuses'],
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
            instance.user.phone_number = (
                user_fields.get("phone_number", instance.user.phone_number)
            )
            if "password" in user_fields:
                instance.user.set_password(user_fields.get("password"))
            instance.user.save()
        if "bonuses" in validated_data:
            raise serializers.ValidationError(self.Errors.CANT_CHANGE_BONUSES)
        return instance
