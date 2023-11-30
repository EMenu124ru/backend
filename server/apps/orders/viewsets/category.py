from rest_framework import decorators, response

from apps.core.viewsets import RetrieveListViewSet
from apps.orders.functions import get_available_dishes
from apps.orders.models import Category, Dish
from apps.orders.permissions import CategoryPermission
from apps.orders.serializers import CategorySerializer, DishSerializer


class CategoryViewSet(RetrieveListViewSet):
    queryset = Category.objects.all()
    permission_classes = (CategoryPermission,)

    def get_serializer_class(self):
        if self.action == "dishes":
            return DishSerializer
        return CategorySerializer

    def get_queryset(self):
        if self.action == "dishes":
            queryset = Dish.objects.prefetch_related("ingredients").filter(
                category_id=self.kwargs["pk"],
            )
            if self.request.user.is_authenticated:
                if not self.request.user.is_client:
                    return get_available_dishes(
                        queryset,
                        self.request.user.employee.restaurant.id,
                    )
            return queryset
        return self.queryset

    @decorators.action(methods=("GET",), detail=True)
    def dishes(self, request, *args, **kwargs) -> response.Response:
        return super().list(request, *args, **kwargs)
