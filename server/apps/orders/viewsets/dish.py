from rest_framework import (
    decorators,
    response,
    status,
)

from apps.core.viewsets import (
    BaseViewSet,
    RetrieveListViewSet,
    DestroyViewSet,
)
from apps.orders.models import (
    Dish,
    Order,
    OrderAndDish,
    Ingredient,
    DishImage,
)
from apps.orders.permissions import (
    DishPermission,
    IngredientPermission,
)
from apps.orders.serializers import (
    DishImageSerializer,
    DishSerializer,
    OrderSerializer,
    IngredientSerializer,
)


class IngredientViewSet(RetrieveListViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IngredientPermission,)


class DishViewSet(BaseViewSet):
    permission_classes = (DishPermission,)

    def get_serializer_class(self):
        if self.action == "orders":
            return OrderSerializer
        return DishSerializer

    def perform_destroy(self, instance) -> None:
        for image in instance.images.all():
            image.image.storage.delete(image.image.path)
        instance.delete()

    def get_queryset(self):
        if self.action == "orders":
            orders = OrderAndDish.objects.filter(
                dish_id=self.kwargs["pk"],
            ).values_list("order_id", flat=True)
            return Order.objects.filter(id__in=orders)
        return Dish.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        dish = Dish.objects.get(id=serializer.data["id"])
        if request.data.get("images", None) is not None:
            serializers = [
                DishImageSerializer(data={
                    "image": image,
                    "dish": dish.pk,
                })
                for image in request.data.pop("images", [])
            ]
            for serializer in serializers:
                serializer.is_valid(raise_exception=True)
                serializer.save()
        return response.Response(
            data=DishSerializer(dish).data,
            status=status.HTTP_201_CREATED,
        )

    @decorators.action(methods=("GET",), detail=True)
    def reviews(self, request, *args, **kwargs) -> response.Response:
        return super().list(request, *args, **kwargs)

    @decorators.action(methods=("GET",), detail=True)
    def orders(self, request, *args, **kwargs) -> response.Response:
        return super().list(request, *args, **kwargs)

    @decorators.action(methods=("POST",), detail=True)
    def images(self, request, *args, **kwargs):
        if request.data.get("images", None) is None:
            return response.Response(
                data={"images": "Изображения отсутствуют"},
                status=status.HTTP_400_BAD_REQUEST,
                exception=True,
            )
        serializers = [
            DishImageSerializer(data={
                "image": image,
                "dish": request.data.get("dish"),
            })
            for image in request.data.pop("images")
        ]
        for serializer in serializers:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        dish = Dish.objects.get(id=request.data.get("dish"))
        return response.Response(
            DishImageSerializer(
                dish.images.all(),
                many=True,
            ).data,
            status=status.HTTP_201_CREATED,
        )


class DishImageViewSet(DestroyViewSet):
    queryset = DishImage.objects.all()
    permission_classes = (DishPermission, )
