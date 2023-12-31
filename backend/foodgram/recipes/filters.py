from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(filters.FilterSet):
    author = filters.CharFilter(field_name='author__id')
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(method='boolean_to_enum')
    is_in_shopping_cart = filters.BooleanFilter(method='boolean_to_enum')

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_in_shopping_cart', 'is_favorited']

    def boolean_to_enum(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            if name == 'is_in_shopping_cart':
                return queryset.filter(in_carts__user=user)
            if name == 'is_favorited':
                return queryset.filter(in_favorites__user=user)
        return queryset
