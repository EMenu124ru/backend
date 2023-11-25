from rest_framework import mixins, viewsets

from apps.core.utils import PaginationObject


class CreateReadUpdateViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """CreateReadUpdate ViewSet for `create`, `retrieve` and `update` actions."""

    pagination_class = PaginationObject
