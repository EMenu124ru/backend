from apps.core.models import ObjectFile

from .base import BaseModelSerializer


class ObjectFileSerializer(BaseModelSerializer):

    class Meta:
        model = ObjectFile
        fields = (
            "file",
            "filename",
        )
