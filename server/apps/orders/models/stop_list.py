from django.db import models


class StopList(models.Model):
    dish = models.ForeignKey(
        "orders.Dish",
        related_name="stop_list",
        on_delete=models.CASCADE,
        verbose_name="Блюда",
    )
    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        on_delete=models.CASCADE,
        related_name="stop_list",
        verbose_name="Ресторан",
    )

    class Meta:
        verbose_name = "Стоп лист ресторана"
        verbose_name_plural = "Стоп листы ресторанов"

    def __str__(self) -> str:
        return f"StopList with dish: {self.dish}, restaurant: {self.restaurant}"
