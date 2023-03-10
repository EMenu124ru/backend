from django.db import models


class Restaurant(models.Model):
    address = models.TextField(
        verbose_name="Адрес",
    )
    reviews = models.ManyToManyField(
        "reviews.Review",
        related_name="restaurant",
        verbose_name="Отзыв",
    )

    class Meta:
        verbose_name = "Ресторан"
        verbose_name_plural = "Рестораны"

    def __str__(self) -> str:
        return f"Restaurant {self.address}"
