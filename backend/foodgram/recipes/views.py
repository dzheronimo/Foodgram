from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework import permissions, status

from .models import Tag, Recipe, Ingredient, FavoriteRecipes, ShoppingCart, IngredientAmountRecipe
from .serializers import (ListTagSerializer, IngredientSerializer, RecipeSerializer, FavoriteRecipeSerializer,
                          ShortRecipeSerializer, SubscriptionSerializer
                          )
from api.views import StandartResultsSetPagination


class PostDestroyModelMixin(
     CreateModelMixin, DestroyModelMixin, GenericViewSet):
    pass


class ListPostDestroyMixin(
     ListModelMixin, PostDestroyModelMixin):
    pass


class ListTagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = ListTagSerializer
    # pagination_class = StandartResultsSetPagination
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
                    {"errors": "Рецепт уже находится в избранном"},
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
                    {"errors": "Рецепт не найден в списке избранных."},
                    status=status.HTTP_400_BAD_REQUEST
                )

    @action(detail=True,
            methods=['POST', 'DELETE', ],
            permission_classes = [permissions.IsAuthenticated, ])
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST' and recipe:
            cart, _ = ShoppingCart.objects.get_or_create(
                user=user,
                recipe=recipe
            )
            if not _:
                return Response(
                    {"errors": "Ингредиенты рецепта уже находятся"
                               "в списке покупок."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = ShortRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        current_cart = ShoppingCart.objects.filter(
            user=user,
            recipe=recipe
        )
        if current_cart.exists():
            current_cart.delete()

            return Response(
                {"shopping_cart": "Ингредиенты рецепты удалены"
                                  "из списка покупок"},
                status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"errors": "Ингредиенты рецепта не находятся в списке покупок"},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False,
            methods=['GET', ])
    def download_shopping_cart(self, request):
        user = request.user
        cart = ShoppingCart.objects.filter(
            user=user
        )
        if cart.exists():
            with open('shopping_cart.txt', mode='w') as file:
                writer = file.write
                writer('lkefvelvmer')
            return Response({"ad": "wef"})


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
