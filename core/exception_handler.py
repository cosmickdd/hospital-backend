from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {
            'success': False,
            'status_code': response.status_code,
            'errors': response.data
        }
    else:
        # Unhandled exceptions
        response = Response({
            'success': False,
            'status_code': 500,
            'errors': 'Internal server error.'
        }, status=500)
    return response
