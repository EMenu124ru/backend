from .category import CategoryAdmin
from .dish import (
    DishAdmin,
    DishImageAdmin,
    IngredientAdmin,
)
from .order import OrderAdmin
from .order_and_dish import OrderAndDishAdmin
from .reservation import ReservationAdmin
from .stop_list import StopListAdmin

__all__ = (
    CategoryAdmin,
    DishAdmin,
    IngredientAdmin,
    DishImageAdmin,
    OrderAdmin,
    OrderAndDishAdmin,
    ReservationAdmin,
    StopListAdmin,
)
