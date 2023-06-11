from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken, BlacklistedToken
)

from api.views import StandartResultsSetPagination


class PaginatedUserViewSet(UserViewSet):
    pagination_class = StandartResultsSetPagination
    serializer_class = AuthorSerializer
