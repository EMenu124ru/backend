from apps.core.models import TagBase


class TagToPlace(TagBase):

    class Meta:
        verbose_name = "Тэг для места"
        verbose_name_plural = "Тэги для места"

    def __str__(self) -> str:
        return (
            "TagToPlace"
            f"(id={self.pk},"
            f"name={self.name})"
        )
