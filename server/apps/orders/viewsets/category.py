from django.shortcuts import get_object_or_404
from rest_framework import decorators, response

from apps.core.viewsets import RetrieveListViewSet
from apps.orders.constants import CacheActions
from apps.orders.functions import get_or_create_cache_dishes
from apps.orders.models import Category
from apps.orders.permissions import CategoryPermission
from apps.orders.serializers import CategorySerializer, DishSerializer
from apps.restaurants.models import Restaurant


class CategoryViewSet(RetrieveListViewSet):
    permission_classes = (CategoryPermission,)

    def paginate_queryset(self, queryset):
        if self.action == "list":
            self.pagination_class = None
        return super().paginate_queryset(queryset)

    def get_serializer_class(self):
        if self.action == "dishes":
            return DishSerializer
        return CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.order_by("name").prefetch_related("dishes")
        if self.action == "dishes":
            category = get_object_or_404(queryset, pk=self.kwargs["pk"])
            restaurant_id = (
                self.request.user.employee.restaurant.id
                if self.request.user.is_authenticated and not self.request.user.is_client
                else self.request.query_params.get("restaurant_id", None)
            )
            if restaurant_id and Restaurant.objects.filter(pk=restaurant_id).exists():
                return get_or_create_cache_dishes(CacheActions.GET, category, restaurant_id)
            return category.dishes.order_by("price")
        return queryset

    @decorators.action(methods=("GET",), detail=True)
    def dishes(self, request, *args, **kwargs) -> response.Response:
        return super().list(request, *args, **kwargs)
