from rest_framework import decorators, response, status

from apps.core.views import CRUDViewSet
from apps.users.models import Client
from apps.users.serializers import ClientSerializer, ClientAuthSerializer
from apps.users.permissions import IsCurrentUser


class ClientViewSet(CRUDViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (IsCurrentUser,)

    def perform_destroy(self, instance):
        instance.user.delete()
        instance.delete()

    @decorators.action(methods=("POST",), detail=False)
    def login(self, request, *args, **kwargs) -> response.Response:
        serializer = ClientAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response.Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
