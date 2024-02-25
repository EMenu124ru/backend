from apps.core.viewsets import ListViewSet, RetrieveViewSet
from apps.orders.models import Dish, Ingredient
from apps.orders.permissions import DishPermission, IngredientPermission
from apps.orders.serializers import DishSerializer, IngredientSerializer


class IngredientViewSet(ListViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IngredientPermission,)


class DishViewSet(RetrieveViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = (DishPermission,)
