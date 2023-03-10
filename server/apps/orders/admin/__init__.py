from .category import CategoryAdmin
from .dish import DishAdmin
from .dish_image import DishImageAdmin
from .order import OrderAdmin
from .order_and_dish import OrderAndDishAdmin
from .restaurant_and_order import RestaurantAndOrderAdmin
from .stop_list import StopListAdmin

__all__ = (
    CategoryAdmin,
    DishAdmin,
    DishImageAdmin,
    OrderAdmin,
    OrderAndDishAdmin,
    RestaurantAndOrderAdmin,
    StopListAdmin,
)
