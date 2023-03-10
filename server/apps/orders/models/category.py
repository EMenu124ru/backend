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
