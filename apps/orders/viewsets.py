from rest_framework import decorators, response, status

from apps.core.views import BaseViewSet, CreateDestroyViewSet

from . import models, serializers


class CategoryViewSet(BaseViewSet):

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

    def get_serializer_class(self):
        # if self.action == "reviews":
        #     return ReviewSerializer
        if self.action == "orders":
            return serializers.OrderSerializer
        return serializers.DishSerializer

    def get_queryset(self):
        if self.action == "reviews":
            return models.Dish.objects.prefetch_related(
                "reviews",
            ).get(id=self.request.parser_context["kwargs"]["pk"]).reviews.all()
        if self.action == "orders":
            return models.Dish.objects.prefetch_related(
                "orders",
            ).get(id=self.request.parser_context["kwargs"]["pk"]).orders.all()
        return models.Dish.objects.all()

    def create(self, request, *args, **kwargs):
        images = request.data.pop("images")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        dish = models.Dish.objects.get(id=serializer.data["id"])
        models.DishImages.objects.bulk_create(
            [
                models.DishImages(
                    image=image,
                    dish=dish,
                )
                for image in images
            ],
        )
        return response.Response(
            serializer.data,
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


class RestaurantAndOrderViewSet(BaseViewSet):

    queryset = models.RestaurantAndOrder.objects.all()
    serializer_class = serializers.RestaurantAndOrderSerializer

    def perform_destroy(self, instance):
        if instance.order:
            instance.order.delete()
        instance.delete()
