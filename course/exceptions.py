from rest_framework import status
from rest_framework.exceptions import APIException


class ContentNotCompleted(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Previous content was not completed.'
