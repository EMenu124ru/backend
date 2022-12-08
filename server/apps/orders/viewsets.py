from rest_framework import decorators, response, status, generics

from apps.core.views import (
    BaseViewSet,
    CreateDestroyViewSet,
    CreateReadUpdateViewSet,
)

from . import models, permissions, serializers


class CategoryViewSet(BaseViewSet):

    permission_classes = (permissions.DishCategoryPermissions,)

    def get_serializer_class(self):
        if self.action == "dishes":
            return serializers.DishSerializer
        return serializers.CategorySerializer

    def get_queryset(self):
        if self.action == "dishes":
            return models.Category.objects.prefetch_related(
                "dishes",
            ).get(id=self.request.parser_context["kwargs"]["pk"]).dishes.all()
        return models.Category.objects.all()

    @decorators.action(methods=("GET",), detail=True)
    def dishes(self, request, *args, **kwargs) -> response.Response:
        return super().list(request, *args, **kwargs)


class DishViewSet(BaseViewSet):

    permission_classes = (permissions.DishCategoryPermissions,)

    def get_serializer_class(self):
        # if self.action == "reviews":
        #     return ReviewSerializer
        if self.action == "orders":
            return serializers.OrderSerializer
        return serializers.DishSerializer

    def perform_destroy(self, instance) -> None:
        for image in instance.images.all():
            image.image.storage.delete(image.image.path)
        instance.delete()

    def get_queryset(self):
        if self.action == "reviews":
            return models.Dish.objects.prefetch_related(
                "reviews",
            ).get(id=self.request.parser_context["kwargs"]["pk"]).reviews.all()
        if self.action == "orders":
            orders = models.Dish.objects.prefetch_related(
                "orders",
            ).get(
                id=self.request.parser_context["kwargs"]["pk"],
            ).orders.all().values_list("order", flat=True)
            return models.Order.objects.filter(id__in=orders)
        return models.Dish.objects.all()

    def create(self, request, *args, **kwargs):
        images = request.data.get("images", [])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        dish = models.Dish.objects.get(id=serializer.data["id"])
        models.DishImages.objects.bulk_create(
            [models.DishImages(image=image, dish=dish) for image in images],
        )
        return response.Response(
            data=serializers.DishSerializer(dish).data,
            status=status.HTTP_201_CREATED,
        )

    @decorators.action(methods=("GET",), detail=True)
    def reviews(self, request, *args, **kwargs) -> response.Response:
        return super().list(request, *args, **kwargs)

    @decorators.action(methods=("GET",), detail=True)
    def orders(self, request, *args, **kwargs) -> response.Response:
        return super().list(request, *args, **kwargs)


class DishImageViewSet(CreateDestroyViewSet):

    queryset = models.DishImages.objects.all()
    permission_classes = (
        permissions.permissions.IsAuthenticated & permissions.DishCategoryPermissions,
    )

    def create(self, request, *args, **kwargs):
        dish = models.Dish.objects.get(id=request.data["dish"])
        models.DishImages.objects.bulk_create(
            [
                models.DishImages(
                    image=image,
                    dish=dish,
                )
                for image in request.data.pop("images")
            ]
        )
        return response.Response(
            serializers.DishImageSerializer(
                dish.images.all(),
                many=True,
            ).data,
            status=status.HTTP_201_CREATED,
        )


class OrderViewSet(BaseViewSet):

    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = (
        permissions.permissions.IsAuthenticated & permissions.OrderPermissions,
    )

    def perform_create(self, serializer) -> None:
        serializer.save(employee=self.request.user.employee)


class RestaurantAndOrderViewSet(BaseViewSet):

    queryset = models.RestaurantAndOrder.objects.all()
    serializer_class = serializers.RestaurantAndOrderSerializer
    permission_classes = (
        permissions.permissions.IsAuthenticated & permissions.RestaurantAndOrdersPermissions,
    )

    def perform_destroy(self, instance):
        if instance.order:
            instance.order.delete()
        instance.delete()


class OrderAndDishesView(generics.UpdateAPIView):
    pass

# статус - изменять - повар
# коммент - 


class StopListViewSet(CreateReadUpdateViewSet):
    pass
# Read - официант
# Create/update - повар
