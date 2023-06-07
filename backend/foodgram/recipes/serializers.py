from django.shortcuts import get_object_or_404
from rest_framework import serializers
from pytils.translit import slugify

from .models import Tag, Ingredient, Recipe, IngredientAmountRecipe, FavoriteRecipes
from users.models import User


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name']


class ListTagSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']

    def get_slug(self, obj):
        slug = slugify(obj.name)
        return slug


# class TagSerializer(serializers.ModelSerializer):
#     id = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all())
#
#     class Meta:
#         model = Tag
#         fields = ['id']


class IngredientAmountRecipeSerializer(serializers.ModelSerializer):
    amount = serializers.ReadOnlyField()
    class Meta:
        model = IngredientAmountRecipe
        fields = ['amount']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class GetRecipeSerializer(serializers.ModelSerializer):
    tags = ListTagSerializer(many=True)
    author = AuthorSerializer()
    ingredients = IngredientSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time']

    def get_is_favorited(self, obj):
        favorites = obj.is_favorite.all()
        if favorites:
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        cart = obj.is_in_shopping_cart.all()
        if cart:
            return True
        return False
