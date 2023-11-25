from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.viewsets import CreateReadUpdateDestroyViewSet
from apps.users.models import Client
from apps.users.permissions import IsCurrentUser
from apps.users.serializers import ClientSerializer


class ClientViewSet(CreateReadUpdateDestroyViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (IsCurrentUser,)

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
        serializer = ClientSerializer(request.user.client)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
