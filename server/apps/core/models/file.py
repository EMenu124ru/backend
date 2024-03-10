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
        super().save(*args, **kwargs)
        init_directories()
        if self.file.name:
            self.filename = self.file.name

    def delete(self, *args, **kwargs):
        self.file.storage.delete(self.file.path)
        super().delete(*args, **kwargs)

    @classmethod
    def create_default_object(cls):
        path = Path(settings.STATIC_ROOT)
        name = "default"
        filename = f"{name}.png"
        default_image = path / "app" / "img" / filename
        if (file := cls.objects.filter(filename=name)) and file.exists():
            return file.first().id
        obj = cls(filename=name)
        with open(default_image.absolute(), mode="rb") as file:
            obj.file.save(name=filename, content=file, save=False)
        obj.filename = name
        obj.save()
        return obj.id
