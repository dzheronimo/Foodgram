from django.db.models import F
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework import permissions

from .models import Tag, Recipe, Ingredient, IngredientAmountRecipe
from .serializers import (ListTagSerializer, IngredientSerializer, CreateRecipeSerializer, GetRecipeSerializer
                          )
from api.views import StandartResultsSetPagination


class ListRetrieveModelMixin(ListModelMixin, RetrieveModelMixin,
                             GenericViewSet):
    pass


class ListTagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = ListTagSerializer
    pagination_class = StandartResultsSetPagination
    permission_classes = [permissions.AllowAny, ]


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny, ]


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = CreateRecipeSerializer
    pagination_class = StandartResultsSetPagination
    permission_classes = [permissions.AllowAny, ]


    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return GetRecipeSerializer
        return CreateRecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CreateRecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = StandartResultsSetPagination
    permission_classes = [permissions.AllowAny, ]



        # if self.request.method == 'POST':
        #     return RecipeCreateSerializer
        # elif self.request.method == 'GET':
        #     return RecipeListRetrieveSerializer



