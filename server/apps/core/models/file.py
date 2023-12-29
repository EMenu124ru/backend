import uuid
from pathlib import Path

from django.conf import settings
from django.db import models


def get_directory_path(instance, _) -> str:
    uuid = str(instance.id)
    return f"{uuid[:2]}/{uuid}"


def init_directories():
    path = Path(settings.MEDIA_ROOT)
    HEXDIGITS = "0123456789abcdef"
    path.mkdir(exist_ok=True, parents=True)
    prefixes = [first + second for first in HEXDIGITS for second in HEXDIGITS]
    for prefix in prefixes:
        (path / prefix).mkdir(exist_ok=True)


class ObjectFile(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    file = models.FileField(
        upload_to=get_directory_path,
        verbose_name="Файл",
    )
    filename = models.TextField(
        default="unnamed_file",
        verbose_name="Название файла",
    )

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"

    def __str__(self) -> str:
        return f"File {self.filename}"

    def save(self, *args, **kwargs):
        init_directories()
        self.filename = self.file.name
        super().save(*args, **kwargs)
