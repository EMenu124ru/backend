from django.db import models


class Review(models.Model):
    review = models.TextField(
        verbose_name="Текст отзыва",
    )
    mark = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        verbose_name="Оценка",
    )
    client = models.ForeignKey(
        "users.Client",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Клиент",
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self) -> str:
        return f"Review {self.review} {self.mark} {self.client}"


class ReviewImages(models.Model):
    image = models.ImageField(
        verbose_name="Картинка"
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Отзыв"
    )

    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"

    def __str__(self) -> str:
        return f"ReviewImages {self.image} {self.review}"


class RestaurantReview(models.Model):
    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Ресторан",
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Отзыв",
    )

    class Meta:
        verbose_name = "Отзыв ресторана"
        verbose_name_plural = "Отзывы ресторанов"

    def __str__(self) -> str:
        return f"RestaurantReview {self.restaurant} {self.review}"


class DishReview(models.Model):
    dish = models.ForeignKey(
        "orders.Dish",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Блюдо",
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Отзыв",
    )

    class Meta:
        verbose_name = "Отзыв блюда"
        verbose_name_plural = "Отзывы блюд"

    def __str__(self) -> str:
        return f"DishReview {self.dish} {self.review}"
