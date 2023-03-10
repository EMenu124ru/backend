from rest_framework import mixins, viewsets


class CreateReadUpdateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """CreateReadUpdateDestroy ViewSet for `create`, `destroy`, `retrieve` and `update` actions."""

    pass
