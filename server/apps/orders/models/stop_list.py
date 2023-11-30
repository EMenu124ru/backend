from django.db import models


class StopList(models.Model):
    ingredient = models.ForeignKey(
        "orders.Ingredient",
        related_name="stop_list",
        on_delete=models.CASCADE,
        verbose_name="Отсутствующие ингредиенты",
    )
    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        on_delete=models.CASCADE,
        related_name="stop_list",
        verbose_name="Ресторан",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время добавления ингредиента",
    )

    class Meta:
        verbose_name = "Стоп лист ресторана"
        verbose_name_plural = "Стоп листы ресторанов"

    def __str__(self) -> str:
        return (
            f"StopList ingredient={self.ingredient}, "
            f"restaurant={self.restaurant}, "
            f"created_at={self.created_at}"
        )
