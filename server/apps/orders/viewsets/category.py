from rest_framework import decorators, response

from apps.core.viewsets import BaseViewSet
from apps.orders.models import Category, Dish
from apps.orders.permissions import CategoryPermission
from apps.orders.serializers import CategorySerializer, DishSerializer


class CategoryViewSet(BaseViewSet):
    permission_classes = (CategoryPermission,)

    def get_serializer_class(self):
        if self.action == "dishes":
            return DishSerializer
        return CategorySerializer

    def get_queryset(self):
        if self.action == "dishes":
            return Dish.objects.filter(category_id=self.kwargs["pk"])
        return Category.objects.all()

    @decorators.action(methods=("GET",), detail=True)
    def dishes(self, request, *args, **kwargs) -> response.Response:
        return super().list(request, *args, **kwargs)
