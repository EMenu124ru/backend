from django.db import models

from apps.core.models import TagBase


class TagToPlace(TagBase):
    class Types(models.TextChoices):
        LOCATION = "LOCATION", "Местоположение"
        NUMBER_OF_SEATS = "NUMBER_OF_SEATS", "Количество мест"

    type = models.CharField(
        max_length=16,
        choices=Types.choices,
        default=Types.LOCATION,
        verbose_name="Тип тэга",
    )

    class Meta:
        verbose_name = "Тэг для места"
        verbose_name_plural = "Тэги для места"

    def __str__(self) -> str:
        return (
            "TagToPlace"
            f"(id={self.pk},"
            f"type={self.type},"
            f"name={self.name})"
        )
