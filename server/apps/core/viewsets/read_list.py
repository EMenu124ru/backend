from rest_framework import mixins, viewsets

from apps.core.services import PaginationObject


class ListViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """RetrieveList ViewSet for `list` action."""

    pagination_class = PaginationObject
