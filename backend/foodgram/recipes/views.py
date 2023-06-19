from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import (
    GenericViewSet, ModelViewSet, ReadOnlyModelViewSet)

from api.paginators import StandartResultsSetPagination

from .filters import IngredientSearchFilter, RecipeFilter
from .models import (FavoriteRecipes, Ingredient, IngredientAmountRecipe,
                     Recipe, ShoppingCart, Tag
                     )
from .serializers import (ListTagSerializer, IngredientSerializer,
                          RecipeSerializer, ShortRecipeSerializer
                          )


class PostDestroyModelMixin(CreateModelMixin,
                            DestroyModelMixin,
                            GenericViewSet):
    pass


class ListPostDestroyMixin(ListModelMixin,
                           PostDestroyModelMixin):
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
    filter_backends = [IngredientSearchFilter, ]
    search_fields = ['$\S+', ]


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = StandartResultsSetPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['author', ]
    filterset_class = RecipeFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    http_method_names = ['get', 'post', 'patch', 'delete', ]

    @action(detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=[permissions.IsAuthenticated, ])
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

        if favorited.exists():
            favorited.delete()
            return Response(
                {"is_favorited": "Рецепт удален из списка избранных."},
                status=status.HTTP_204_NO_CONTENT)

        return Response(
            {"errors": "Рецепт не найден в списке избранных."},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True,
            methods=['POST', 'DELETE', ],
            permission_classes=[permissions.IsAuthenticated, ])
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST' and recipe:
            cart, created = ShoppingCart.objects.get_or_create(
                user=user,
                recipe=recipe
            )
            if not created:
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

    def ingredients_to_list(self, carts):
        """Возвращает словарь со списком ингредиентов и количеством"""
        recipes = [cart.recipe for cart in carts]
        all_ingredients = Ingredient.objects.all()
        amount_ingredients = [0] * max(
            [ingredient.id for ingredient in all_ingredients]
        )
        for recipe in recipes:
            ingredient_amount = IngredientAmountRecipe.objects.filter(
                recipe=recipe
            )
            for ingredient in ingredient_amount:
                ingredient_id = ingredient.ingredient.id
                amount_ingredients[ingredient_id] += ingredient.amount

        to_response = {}

        for id_ingredient in range(len(amount_ingredients)):
            if amount_ingredients[id_ingredient]:
                ingredient = Ingredient.objects.get(id=id_ingredient)

                to_response[ingredient.name] = (
                    f'{amount_ingredients[id_ingredient]} '
                    f'{ingredient.measurement_unit}')
        return to_response

    @action(detail=False,
            methods=['GET', ],
            permission_classes=[permissions.IsAuthenticated, ])
    def download_shopping_cart(self, request):
        user = request.user
        carts = ShoppingCart.objects.filter(
            user=user
        )

        if carts.exists():
            shopping_list = self.ingredients_to_list(carts)
            file_name = f'{self.request.user}'
            with open(f'{file_name}_shopping_cart.txt', mode='w') as file:
                writer = file.write
                writer('\n'.join(
                    f'◯ {name} - {amount}' for name, amount
                    in shopping_list.items()))
            return FileResponse(
                open(f'{file_name}_shopping_cart.txt', mode='rb')
            )
        return Response(
            {"errors": "Список покупок пуст."},
            status=status.HTTP_400_BAD_REQUEST
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
