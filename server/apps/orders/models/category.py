from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name="Название",
    )
    icon = models.ForeignKey(
        "core.ObjectFile",
        on_delete=models.CASCADE,
        verbose_name="Иконка",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return (
            "Category"
            f"(id={self.pk},"
            f"name={self.name})"
        )
