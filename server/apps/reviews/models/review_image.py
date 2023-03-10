from django.db import models


def get_directory_path(instance, filename) -> str:
    return f"reviews/{instance.review.id}/{filename}"


class ReviewImage(models.Model):
    image = models.ImageField(
        upload_to=get_directory_path,
        verbose_name="Картинка"
    )
    review = models.ForeignKey(
        "reviews.Review",
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Отзыв",
    )

    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"

    def __str__(self) -> str:
        return f"ReviewImage {self.image} {self.review}"
