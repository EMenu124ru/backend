from rest_framework import mixins, viewsets

from apps.core.utils import PaginationObject


class RetrieveViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """RetrieveList ViewSet for `retrieve` action."""

    pagination_class = PaginationObject


class RetrieveListViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """RetrieveList ViewSet for `list`, `retrieve` action."""

    pagination_class = PaginationObject


class ListViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """RetrieveList ViewSet for `list` action."""

    pagination_class = PaginationObject
