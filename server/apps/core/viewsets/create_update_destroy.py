from rest_framework import mixins, viewsets


class CreateUpdateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """CreateUpdateDestroy ViewSet for `create` and `update` and `destroy` actions."""
