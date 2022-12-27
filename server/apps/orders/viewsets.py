from rest_framework import decorators, permissions, response, status

from apps.core.views import (
    BaseViewSet,
    CreateDestroyViewSet,
    CreateReadDeleteViewSet,
    CreateUpdateDestroyViewSet,
)

from .models import (
    Category,
    Dish,
    DishImages,
    Order,
    OrderAndDishes,
    RestaurantAndOrder,
    StopList,
)
from .permissions import (
    DishCategoryPermissions,
    OrderAndDishesPermission,
    OrderPermissions,
    RestaurantAndOrdersPermissions,
    StopListPermission,
)
from .serializers import (
    CategorySerializer,
    DishImageSerializer,
    DishSerializer,
    OrderAndDishSerializer,
    OrderSerializer,
    RestaurantAndOrderSerializer,
    StopListSerializer,
)


class CategoryViewSet(BaseViewSet):

    permission_classes = (DishCategoryPermissions,)

    def get_serializer_class(self):
        if self.action == "dishes":
            return DishSerializer
        return CategorySerializer

    def get_queryset(self):
        if self.action == "dishes":
            return Category.objects.prefetch_related(
                "dishes",
            ).get(id=self.kwargs["pk"]).dishes.all()
        return Category.objects.all()

    @decorators.action(methods=("GET",), detail=True)
    def dishes(self, request, *args, **kwargs) -> response.Response:
        return super().list(request, *args, **kwargs)


class DishViewSet(BaseViewSet):

    permission_classes = (DishCategoryPermissions,)

    def get_serializer_class(self):
        # if self.action == "reviews":
        #     return ReviewSerializer
        if self.action == "orders":
            return OrderSerializer
        return DishSerializer

    def perform_destroy(self, instance) -> None:
        for image in instance.images.all():
            image.image.storage.delete(image.image.path)
        instance.delete()

    def get_queryset(self):
        if self.action == "reviews":
            return Dish.objects.prefetch_related(
                "reviews",
            ).get(id=self.kwargs["pk"]).reviews.all()
        if self.action == "orders":
            orders = Dish.objects.prefetch_related(
                "orders",
            ).get(
                id=self.kwargs["pk"],
            ).orders.all().values_list("order", flat=True)
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


class DishImageViewSet(CreateDestroyViewSet):

    queryset = DishImages.objects.all()
    permission_classes = (
        permissions.IsAuthenticated & DishCategoryPermissions,
    )

    def create(self, request, *args, **kwargs):
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


class OrderViewSet(BaseViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (
        permissions.IsAuthenticated & OrderPermissions,
    )

    def perform_create(self, serializer) -> None:
        serializer.save(employee=self.request.user.employee)


class RestaurantAndOrderViewSet(BaseViewSet):

    queryset = RestaurantAndOrder.objects.all()
    serializer_class = RestaurantAndOrderSerializer
    permission_classes = (
        permissions.IsAuthenticated & RestaurantAndOrdersPermissions,
    )

    def perform_destroy(self, instance) -> None:
        if instance.order:
            instance.order.delete()
        instance.delete()


class OrderAndDishesViewSet(CreateUpdateDestroyViewSet):

    queryset = OrderAndDishes.objects.all()
    serializer_class = OrderAndDishSerializer
    permission_classes = (
        permissions.IsAuthenticated & OrderAndDishesPermission,
    )


class StopListViewSet(CreateReadDeleteViewSet):

    serializer_class = StopListSerializer
    permission_classes = (
        permissions.IsAuthenticated & StopListPermission,
    )

    def get_queryset(self):
        if self.action == "list":
            return StopList.objects.filter(
                restaurant=self.request.user.employee.restaurant,
            )
        return StopList.objects.all()
