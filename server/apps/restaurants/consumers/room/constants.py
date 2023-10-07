from typing import Final


class Actions:
    EMPLOYEE_ORDERS_LIST: Final[str] = "employee_orders_list"
    CREATE_ORDER: Final[str] = "create_order"
    EDIT_ORDER: Final[str] = "edit_order"


class Events:
    EMPLOYEE_ORDERS_RETRIEVE: Final[str] = "employee_orders_retrieve"
    CREATE_ORDER: Final[str] = "create_order"
    CREATE_ORDER_USER: Final[str] = "create_order_user"
    EDIT_ORDER: Final[str] = "edit_order"
    EDIT_ORDER_USER: Final[str] = "edit_order_user"
