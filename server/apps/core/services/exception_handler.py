from typing import Union

from rest_framework.exceptions import ErrorDetail
from rest_framework.views import exception_handler


def iterate_by_errors(errors: list, dict_errors: dict):
    """Func for iterate by errors"""
    for key, value in dict_errors.items():
        if isinstance(value, (list, dict)):
            errors.extend(check_errors_dict(key, value))
        else:
            errors.append(value)


def check_errors_dict(
    key: str,
    lst_errors: Union[list, dict],
) -> Union[str, list]:
    errors = []
    """Function for recursive error traversal"""
    if isinstance(lst_errors, dict):
        iterate_by_errors(errors, lst_errors)
    elif isinstance(lst_errors, list):
        for data in lst_errors:
            if isinstance(data, ErrorDetail):
                return (
                    [str(data)]
                    if key == "non_field_errors"
                    else [f"{key} - {data}"]
                )
            iterate_by_errors(errors, data)
    return errors


def get_errors(data: list | dict):
    """Entrypoint for get errors"""
    errors = []
    if isinstance(data, list):
        errors.append(data[0])
    elif isinstance(data, dict):
        iterate_by_errors(errors, data)
    return errors


def custom_exception_handler(exc, context):
    """Custom exception handler"""
    response = exception_handler(exc, context)
    if response is not None:
        errors = get_errors(response.data)
        response.data = {"message": "\n".join(map(str, set(errors)))}
    return response
