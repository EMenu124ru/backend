from typing import Final


class Actions:
    EMPLOYEE_ORDERS_LIST: Final[str] = "employee_orders_list"
    CREATE_ORDER: Final[str] = "create_order"
    EDIT_ORDER: Final[str] = "edit_order"


class Events:
    LIST_ORDERS: Final[str] = "list_orders"


class Errors:
    CANT_CREATE_ORDER: Final[str] = "Вы не можете создать заказ"
    CANT_EDIT_ORDER: Final[str] = (
        "Вы не можете редактировать заказ. "
        "Разрешено редактирование статусов готовности блюд в заказе"
    )
