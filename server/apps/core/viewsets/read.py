from rest_framework import mixins, viewsets

from apps.core.utils import PaginationObject


class RetrieveViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """RetrieveList ViewSet for `retrieve` action."""

    pagination_class = PaginationObject
