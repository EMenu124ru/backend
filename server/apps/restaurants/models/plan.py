from django.db import models


class Plan(models.Model):
    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        on_delete=models.CASCADE,
        related_name="plans",
        verbose_name="Ресторан",
    )
    plan = models.TextField(
        verbose_name="План ресторана",
    )

    class Meta:
        verbose_name = "План ресторана"
        verbose_name_plural = "Планы ресторанов"

    def __str__(self) -> str:
        return f"Plan of {self.restaurant}"
