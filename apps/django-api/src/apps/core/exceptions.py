from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """Custom exception handler that returns consistent error responses."""
    response = exception_handler(exc, context)

    if response is not None:
        errors = response.data
        custom_response = {
            "success": False,
            "status_code": response.status_code,
            "message": _get_error_message(response.status_code),
            "errors": errors,
        }
        response.data = custom_response

    return response


def _get_error_message(status_code: int) -> str:
    """Get a human-readable error message for a status code."""
    messages = {
        status.HTTP_400_BAD_REQUEST: "Bad request. Please check your input.",
        status.HTTP_401_UNAUTHORIZED: "Authentication required.",
        status.HTTP_403_FORBIDDEN: "You do not have permission to perform this action.",
        status.HTTP_404_NOT_FOUND: "Resource not found.",
        status.HTTP_405_METHOD_NOT_ALLOWED: "Method not allowed.",
        status.HTTP_409_CONFLICT: "Resource conflict.",
        status.HTTP_429_TOO_MANY_REQUESTS: "Too many requests. Please try again later.",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal server error.",
    }
    return messages.get(status_code, "An error occurred.")
