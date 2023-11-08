from django.db import models


class TagBase(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name="Название тэга"
    )

    class Meta:
        abstract = True
