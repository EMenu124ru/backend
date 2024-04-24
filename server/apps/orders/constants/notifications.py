import enum


class NotificationText(enum.Enum):
    STOP_LIST_ADD = ("Изменение стоп-листа", "Ингредиент {} добавлен в стоп-лист")
    STOP_LIST_REMOVE = ("Изменение стоп-листа", "Ингредиент {} удален из стоп-листа")
    ORDER_NEW = ("Новый заказ", "Появился заказ №{}")
    ORDER_UPDATED = ("Обновление заказа", "Заказ №{} имеет статус {}")

    def __init__(self, title, body):
        self.title = title
        self.body = body
