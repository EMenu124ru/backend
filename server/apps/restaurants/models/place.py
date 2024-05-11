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
    tags = models.ManyToManyField(
        "restaurants.TagToPlace",
        related_name="places",
        verbose_name="Тэги к столу",
    )

    class Meta:
        verbose_name = "Место в ресторане"
        verbose_name_plural = "Места в ресторане"
        unique_together = ('place', 'restaurant')

    def __str__(self) -> str:
        return (
            "Place"
            f"(id={self.pk},"
            f"place={self.place},"
            f"restaurant_id={self.restaurant.pk},"
            f"tags={';'.join([tag.name for tag in self.tags.all()])})"
        )
