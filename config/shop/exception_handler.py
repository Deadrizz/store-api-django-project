from rest_framework.views import exception_handler as drf_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound, NotAuthenticated, PermissionDenied

def custom_exception_handler(exc, context):
    if isinstance(exc, ValidationError):
        if isinstance(exc.detail, dict):
            key, msg = next(iter(exc.detail.items()))
            msg = msg[0] if isinstance(msg, list) else msg
        else:
            key, msg = "detail", str(exc.detail)
        return Response({"detail": msg, "key": key}, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, NotFound):
        return Response({"detail": str(exc), "key": "object"}, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, (NotAuthenticated, PermissionDenied)):
        return Response({"detail": str(exc), "key": "auth"}, status=status.HTTP_401_UNAUTHORIZED)

    response = drf_handler(exc, context)
    if response is not None:
        response.data["status_code"] = response.status_code
    return response