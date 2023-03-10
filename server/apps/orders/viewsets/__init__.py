from .category import CategoryViewSet
from .dish import DishViewSet
from .dish_image import DishImageViewSet
from .order import OrderViewSet
from .order_and_dish import OrderAndDishViewSet
from .restaurant_and_order import RestaurantAndOrderViewSet
from .stop_list import StopListViewSet

__all__ = (
    CategoryViewSet,
    DishViewSet,
    DishImageViewSet,
    OrderViewSet,
    OrderAndDishViewSet,
    RestaurantAndOrderViewSet,
    StopListViewSet,
)
