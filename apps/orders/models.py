from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name="Название",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return f"Category {self.name}"


class Dish(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Категория",
    )
    name = models.CharField(
        max_length=128,
        verbose_name="Название",
    )
    description = models.TextField(
        verbose_name="Описание",
    )
    price = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        verbose_name="Цена",
    )

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"

    def __str__(self) -> str:
        return f"Dish {self.name} {self.category} {self.price} {self.description}"


class Order(models.Model):
    price = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        verbose_name="Цена",
    )
    comment = models.TextField(
        verbose_name="Комментарий",
    )
    employee = models.ForeignKey(
        "users.Employee",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Сотрудник",
    )
    place_number = models.IntegerField(
        verbose_name="Номер места"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self) -> str:
        return f"Order {self.price} {self.comment} {self.employee} {self.place_number}"


class OrderDishes(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Заказ",
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Блюдо",
    )

    class Meta:
        verbose_name = "Блюда в заказе"
        verbose_name_plural = "Блюда в заказах"

    def __str__(self) -> str:
        return f"Order {self.order} {self.dish}"


class OrderClient(models.Model):
    client = models.ForeignKey(
        "users.Client",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Клиент",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Заказ",
    )

    class Meta:
        verbose_name = "Клиент, сделавший заказ"
        verbose_name_plural = "Клиенты, сделавшие заказ"

    def __str__(self) -> str:
        return f"Order {self.client} {self.order}"


class DishImages(models.Model):
    image = models.ImageField(
        verbose_name="Картинка",
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Блюдо",
    )

    class Meta:
        verbose_name = "Картинка блюда"
        verbose_name_plural = "Картинки блюд"

    def __str__(self) -> str:
        return f"Order {self.dish}"


class RestaurantAndOrder(models.Model):
    arrival_time = models.DateTimeField(
        verbose_name="Время прибытия",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Заказ",
    )
    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Ресторан",
    )

    class Meta:
        verbose_name = "Ресторан и заказ"
        verbose_name_plural = "Ресторан и заказы"

    def __str__(self) -> str:
        return f"Order {self.arrival_time} {self.order} {self.restaurant}"
