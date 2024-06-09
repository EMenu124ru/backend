from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.viewsets import CreateReadUpdateDestroyViewSet
from apps.users.models import Client, User
from apps.users.permissions import IsCurrentUser
from apps.users.serializers import ClientSerializer


class ClientViewSet(CreateReadUpdateDestroyViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (IsCurrentUser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_data = serializer.validated_data.get('user')

            if User.objects.filter(phone_number=user_data["phone_number"]).count() > 0:
                return Response(
                    [{"field": "phone_number", "message": "Пользователь с данным номером телефона уже существует"}],
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

            username = (
                f"{user_data['first_name']}_{user_data['last_name']}"
                f"_{user_data['surname']}_{user_data['phone_number']}"
            )
            if User.objects.filter(username=username).count() > 0:
                return Response(
                    [{"field": "username", "message": "Пользователь с данными ФИО и номером телефона уже существует"}],
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def perform_destroy(self, instance):
        instance.user.delete()
        instance.delete()

    @action(methods=("GET",), detail=False)
    def me(self, request, *args, **kwargs) -> Response:
        if not request.user.is_authenticated:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if not request.user.is_client:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer_class()(request.user.client)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
