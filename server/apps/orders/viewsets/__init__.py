from .category import CategoryViewSet
from .dish import DishViewSet, IngredientViewSet
from .order import OrderViewSet
from .order_and_dish import OrderAndDishViewSet
from .reservation import ReservationViewSet
from .stop_list import StopListViewSet

__all__ = (
    CategoryViewSet,
    DishViewSet,
    IngredientViewSet,
    OrderViewSet,
    OrderAndDishViewSet,
    ReservationViewSet,
    StopListViewSet,
)
