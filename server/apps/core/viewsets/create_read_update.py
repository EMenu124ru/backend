from rest_framework import mixins, viewsets


class CreateReadUpdateViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """CreateReadUpdate ViewSet for `create`, `retrieve` and `update` actions."""

    pass
