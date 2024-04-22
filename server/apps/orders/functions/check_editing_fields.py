from collections import OrderedDict


def check_fields(instance, fields: list[str], data: OrderedDict) -> bool:
    for field in fields:
        data.pop(field, None)
    return all([
        instance.__getattribute__(key) == value
        for key, value in data.items()
    ])
