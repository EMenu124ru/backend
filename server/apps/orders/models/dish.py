from django.core.validators import MinValueValidator
from django.db import models

from apps.core.models import TagBase


class Ingredient(TagBase):
    dishes = models.ManyToManyField(
        "orders.Dish",
        related_name="ingredients",
        verbose_name="Блюда с данным ингредиентом",
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self) -> str:
        return (
            "Ingredient"
            f"(id={self.pk},"
            f"name={self.name})"
        )


class Dish(models.Model):
    category = models.ForeignKey(
        "orders.Category",
        on_delete=models.CASCADE,
        related_name="dishes",
        verbose_name="Категория",
    )
    name = models.CharField(
        max_length=128,
        verbose_name="Название",
    )
    description = models.TextField(
        verbose_name="Полное описание",
    )
    short_description = models.TextField(
        verbose_name="Краткое описание",
    )
    price = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Цена",
    )
    weight = models.DecimalField(
        max_digits=11,
        decimal_places=3,
        validators=[MinValueValidator(0)],
        verbose_name="Вес блюда",
    )

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"

    def __str__(self) -> str:
        return (
            "Dish"
            f"(id={self.pk},"
            f"name={self.name},"
            f"category_id={self.category.pk},"
            f"price={self.price},"
            f"description={self.description},"
            f"short_description={self.short_description},"
            f"weight={self.weight})"
        )


class DishImage(models.Model):
    image = models.ForeignKey(
        "core.ObjectFile",
        on_delete=models.CASCADE,
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
        return (
            "DishImage"
            f"(id={self.id},"
            f"dish_id={self.dish.pk})"
        )
