from django.db import models


class Place(models.Model):
    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        on_delete=models.CASCADE,
        related_name="places",
        verbose_name="Ресторан",
    )
    place = models.CharField(
        max_length=16,
        verbose_name="Название места",
    )

    class Meta:
        verbose_name = "Место в ресторане"
        verbose_name_plural = "Места в ресторане"

    def __str__(self) -> str:
        return f"Place {self.place} of {self.restaurant}"
