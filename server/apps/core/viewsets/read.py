from rest_framework import mixins, viewsets

from apps.core.utils import PaginationObject


class RetrieveListViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """RetrieveList ViewSet for `list`, `retrieve` action."""

    pagination_class = PaginationObject
