from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        customized_response = {
            'errors': [value for _, value in response.data.items()]
        }
        response.data = customized_response
    return response
