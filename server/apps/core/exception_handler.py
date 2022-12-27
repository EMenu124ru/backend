from typing import Union

from rest_framework.exceptions import ErrorDetail
from rest_framework.views import exception_handler


def check_errors_dict(key: str, lst_errors: dict) -> Union[str, list]:
    """Function for recursive error traversal"""
    errors = []
    if isinstance(lst_errors, dict):
        for key, value in lst_errors.items():
            if isinstance(value, list) or isinstance(value, dict):
                errors.extend(check_errors_dict(key, value))
            else:
                errors.append(value)
    elif isinstance(lst_errors, list):
        for data in lst_errors:
            if isinstance(data, ErrorDetail):
                return (
                    [str(data)]
                    if key == "non_field_errors"
                    else [f"{key} - {data}"]
                )
            for key, value in data.items():
                if isinstance(value, list) or isinstance(value, dict):
                    errors.extend(check_errors_dict(key, value))
                else:
                    errors.append(value)
    return errors


def custom_exception_handler(exc, context):
    """Custom exception handler"""
    response = exception_handler(exc, context)
    if response is not None:
        errors = []
        for key, value in response.data.items():
            if isinstance(value, list) or isinstance(value, dict):
                errors.extend(check_errors_dict(key, value))
            else:
                errors.append(value)
        response.data = {"message": "\n".join(map(str, set(errors)))}
    return response
