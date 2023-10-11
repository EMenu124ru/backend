from typing import Final


class Actions:
    EMPLOYEE_ORDERS_LIST: Final[str] = "employee_orders_list"
    CREATE_ORDER: Final[str] = "create_order"
    EDIT_ORDER: Final[str] = "edit_order"


class Events:
    LIST_ORDERS: Final[str] = "list_orders"
    NEW_ORDER: Final[str] = "new_order"
    ORDER_CHANGED: Final[str] = "order_changed"
