from rest_framework import mixins, viewsets


class DestroyViewSet(
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Destroy ViewSet for `destroy` action."""
