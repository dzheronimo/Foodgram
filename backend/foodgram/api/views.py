from rest_framework_simplejwt.tokens import BlacklistMixin
from rest_framework.pagination import PageNumberPagination


class StandartResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    # max_page_size = 10

