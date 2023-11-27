from rest_framework import mixins, viewsets

from apps.core.services.pagination import PaginationObject


class RetrieveListViewSet(
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """RetrieveList ViewSet for `list` action."""

    pagination_class = PaginationObject
