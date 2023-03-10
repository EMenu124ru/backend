from django.db import models


def get_directory_path(instance, filename) -> str:
    return (
        f"dishes/{instance.dish.name.replace(' ', '_')}"
        f"_{instance.dish.id}/{filename}"
    )


class DishImage(models.Model):
    image = models.ImageField(
        upload_to=get_directory_path,
        verbose_name="Картинка",
    )
    dish = models.ForeignKey(
        "orders.Dish",
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Блюдо",
    )

    class Meta:
        verbose_name = "Картинка блюда"
        verbose_name_plural = "Картинки блюд"

    def __str__(self) -> str:
        return f"DishImage {self.dish}"
