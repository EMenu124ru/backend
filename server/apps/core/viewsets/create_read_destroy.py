from rest_framework import mixins, viewsets

from apps.core.utils import PaginationObject


class CreateReadDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """CreateReadDestroy ViewSet for `create`, `read`, `destroy` actions."""

    pagination_class = PaginationObject
