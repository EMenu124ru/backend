from django.shortcuts import get_object_or_404
from rest_framework import decorators, response

from apps.core.viewsets import RetrieveListViewSet
from apps.orders.functions import get_available_dishes
from apps.orders.models import Category
from apps.orders.permissions import CategoryPermission
from apps.orders.serializers import CategorySerializer, DishSerializer


class CategoryViewSet(RetrieveListViewSet):
    permission_classes = (CategoryPermission,)

    def get_serializer_class(self):
        if self.action == "dishes":
            return DishSerializer
        return CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all().prefetch_related("dishes")
        if self.action == "dishes":
            category = get_object_or_404(queryset, pk=self.kwargs["pk"])
            queryset = category.dishes.all()
            if self.request.user.is_authenticated:
                if not self.request.user.is_client:
                    return get_available_dishes(
                        queryset,
                        self.request.user.employee.restaurant.id,
                    )
            return queryset
        return queryset

    @decorators.action(methods=("GET",), detail=True)
    def dishes(self, request, *args, **kwargs) -> response.Response:
        return super().list(request, *args, **kwargs)
