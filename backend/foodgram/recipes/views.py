from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework import permissions, status

from .models import Tag, Recipe, Ingredient, FavoriteRecipes
from .serializers import (ListTagSerializer, IngredientSerializer, RecipeSerializer, FavoriteRecipeSerializer,
                          ShortRecipeSerializer
                          )
from api.views import StandartResultsSetPagination


class PostDestroyModelMixin(
        CreateModelMixin, DestroyModelMixin, GenericViewSet):
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
    serializer_class = RecipeSerializer
    pagination_class = StandartResultsSetPagination
    permission_classes = [permissions.AllowAny, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


