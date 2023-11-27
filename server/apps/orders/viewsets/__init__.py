from .category import CategoryViewSet
from .dish import DishViewSet, IngredientPermission, DishImageViewSet
from .order import OrderViewSet
from .order_and_dish import OrderAndDishViewSet
from .reservation import ReservationViewSet
from .stop_list import StopListViewSet

__all__ = (
    CategoryViewSet,
    DishViewSet,
    DishImageViewSet,
    IngredientPermission,
    OrderViewSet,
    OrderAndDishViewSet,
    ReservationViewSet,
    StopListViewSet,
)
