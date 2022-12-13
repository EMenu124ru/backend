from rest_framework import decorators, response, status

from apps.core.views import CRUDViewSet

from . import models, permissions, serializers


class ClientViewSet(CRUDViewSet):

    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer
    permission_classes = (
        permissions.IsCurrentUser,
    )

    def perform_destroy(self, instance):
        instance.user.delete()
        instance.delete()

    @decorators.action(methods=("POST",), detail=False)
    def login(self, request, *args, **kwargs) -> response.Response:
        serializer = serializers.ClientAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response.Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
