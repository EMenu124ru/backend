from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Review(models.Model):
    review = models.TextField(
        verbose_name="Текст отзыва",
    )
    mark = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        verbose_name="Оценка",
    )
    client = models.ForeignKey(
        "users.Client",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="reviews",
        verbose_name="Клиент",
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self) -> str:
        return f"Review {self.review} {self.mark} {self.client}"
