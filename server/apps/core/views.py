from rest_framework import mixins, viewsets

from apps.core.services.pagination import PaginationObject


class BaseViewSet(viewsets.ModelViewSet):
    """Base ViewSet for other views."""

    pagination_class = PaginationObject


class CreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """CreateDestroy ViewSet for `create` and `destroy` actions."""

    pass


class CRUDViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """CRUD ViewSet for `create`, `destroy`, `retrieve` and `update` actions."""

    pass
