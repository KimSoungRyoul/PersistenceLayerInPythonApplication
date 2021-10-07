from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details


class DomainException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail, code=None):
        if code is None:
            code = self.default_code
        self.detail = _get_error_details(detail, code)




