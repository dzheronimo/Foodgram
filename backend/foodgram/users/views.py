from djoser.views import UserViewSet

from recipes.serializers import AuthorSerializer
from api.views import StandartResultsSetPagination


class PaginatedUserViewSet(UserViewSet):
    pagination_class = StandartResultsSetPagination
    serializer_class = AuthorSerializer
