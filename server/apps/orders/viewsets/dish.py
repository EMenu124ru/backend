from apps.core.viewsets import ListViewSet, RetrieveListViewSet
from apps.orders.functions import get_available_dishes
from apps.orders.models import Dish, Ingredient
from apps.orders.permissions import DishPermission, IngredientPermission
from apps.orders.serializers import DishSerializer, IngredientSerializer


class IngredientViewSet(ListViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IngredientPermission,)


class DishViewSet(RetrieveListViewSet):
    serializer_class = DishSerializer
    permission_classes = (DishPermission,)

    def get_queryset(self):
        queryset = Dish.objects.prefetch_related("ingredients").all()
        if (
            self.request.user.is_authenticated and
            not self.request.user.is_client
        ):
            return get_available_dishes(
                queryset,
                self.request.user.employee.restaurant.id,
            )
        return queryset
