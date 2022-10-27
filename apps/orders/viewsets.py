from apps.core.views import BaseViewSet

from . import models, serializers


class CategoryViewSet(BaseViewSet):

    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class DishViewSet(BaseViewSet):

    queryset = models.Dish.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return serializers.DishCreateSerializer
        return serializers.DishRetrieveSerializer


class OrderViewSet(BaseViewSet):

    queryset = models.Order.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return serializers.OrderCreateSerializer
        return serializers.OrderRetrieveSerializer


class RestaurantAndOrderViewSet(BaseViewSet):

    queryset = models.RestaurantAndOrder.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return serializers.RestaurantAndOrderCreateSerializer
        return serializers.RestaurantAndOrderRetrieveSerializer

    def perform_destroy(self, instance):
        if instance.order:
            instance.order.delete()
        instance.delete()
