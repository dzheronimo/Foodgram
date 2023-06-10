from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework import permissions, status

from users.models import User
from .models import Tag, Recipe, Ingredient, FavoriteRecipes, Subscription
from .serializers import (ListTagSerializer, IngredientSerializer, RecipeSerializer, FavoriteRecipeSerializer,
                          ShortRecipeSerializer, SubscriptionSerializer
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

    @action(detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=[permissions.AllowAny, ])
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorited = FavoriteRecipes.objects.filter(user=user, recipe=recipe)

        if request.method == 'POST':
            if favorited.exists():
                return Response(
                    {"is_favorited": "Рецепт уже находится в избранном"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            FavoriteRecipes.objects.create(user=user, recipe=recipe)
            serializer = ShortRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if favorited.exists():
                favorited.delete()
                return Response(
                    {"is_favorited": "Рецепт удален из списка избранных."},
                    status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {"is_favorited": "Рецепт не найден в списке избранных."},
                    status=status.HTTP_400_BAD_REQUEST
                )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
