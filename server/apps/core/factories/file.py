from factory import Faker
from factory.django import DjangoModelFactory, FileField

from apps.core.models import ObjectFile


class ObjectFileFactory(DjangoModelFactory):
    """Factory for ObjectFile instance."""

    id = Faker(
        'uuid4',
    )
    file = FileField()

    class Meta:
        model = ObjectFile
