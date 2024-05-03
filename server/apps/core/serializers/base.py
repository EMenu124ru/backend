from collections import OrderedDict

from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    """Serializer with common logic."""

    def __init__(self, *args, **kwargs):
        """Set current user."""
        super().__init__(*args, **kwargs)
        self._request = self.context.get("request")
        self._user = getattr(self._request, "user", None)
        if self._user is None:
            self._user = self.context.get("user", None)

    def check_fields(self, role: str, data: OrderedDict) -> bool:
        for field in self.Meta.editable_fields.get(role, []):
            data.pop(field, None)
        return all([
            self.instance.__getattribute__(key) == value
            for key, value in data.items()
        ])
