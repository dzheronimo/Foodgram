from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken, BlacklistedToken
)

from api.views import StandartResultsSetPagination

from djoser.views import UserViewSet


class PaginatedUserViewSet(UserViewSet):
    pagination_class = StandartResultsSetPagination
