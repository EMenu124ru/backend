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


class CreateReadDeleteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """CreateReadDeleteViewSet ViewSet for `create`, `read`, `destroy` actions."""

    pagination_class = PaginationObject


class CreateUpdateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """CreateUpdateDestroy ViewSet for `create` and `update` and `destroy` actions."""

    pass


class DestroyViewSet(
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Destroy ViewSet for `destroy` action."""
    pass
