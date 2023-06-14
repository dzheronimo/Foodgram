import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import (
    Tag, Ingredient, Recipe, IngredientAmountRecipe,
    FavoriteRecipes, Subscription
)
from users.models import User


class AuthorSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed']

    def get_is_subscribed(self, obj):
        if self.context:
            user = self.context.get('request').user
            if user.is_authenticated:
                subscription = Subscription.objects.filter(
                    user=user,
                    author=obj
                )
                if subscription.exists():
                    return True
        return False


class ListTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class IngredientAmountRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientAmountRecipe
        fields = ['id', 'name', 'measurement_unit', 'amount', ]


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class RecipeSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    tags = ListTagSerializer(many=True, read_only=True)
    author = AuthorSerializer(read_only=True)
    image = Base64ImageField()
    text = serializers.CharField()
    cooking_time = serializers.IntegerField()
    ingredients = IngredientAmountRecipeSerializer(
        source='amount_ingredient', many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = IngredientAmountRecipe
        fields = ['id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time']

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')

        if not ingredients:
            raise serializers.ValidationError(
                {"ingredients": "Для рецепта требуется"
                                "минимум один ингредиент"}
            )
        for ingredient in ingredients:
            if not Ingredient.objects.filter(pk=ingredient.get('id')):
                raise serializers.ValidationError(
                    {"ingreients": "Можно выбрать только "
                                   "существующий ингредиент!"}
                )
        for tag in tags:
            if not Tag.objects.filter(pk=tag):
                raise serializers.ValidationError(
                    {"tags": "Можно выбрать только "
                                   "существующий тег!"}
                )
        if not tags:
            raise serializers.ValidationError(
                {"tags": "Для рецепта требуется минимум один tag"}
            )
        data['ingredients'] = ingredients
        data['tags'] = tags

        return data

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            IngredientAmountRecipe.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            )

        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.image = validated_data.get('image', instance.image)

        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            instance.tags.set(tags_data)
        if 'ingredients' in validated_data:
            IngredientAmountRecipe.objects.filter(recipe=instance).delete()
            ingredients_data = validated_data.pop('ingredients')
            for ingredient in ingredients_data:
                ingredient_instance = get_object_or_404(
                    Ingredient, pk=ingredient.get('id')
                )
                if ingredient_instance:
                    IngredientAmountRecipe.objects.create(
                        recipe=instance,
                        ingredient=ingredient_instance,
                        amount=ingredient.get('amount')
                    )

        instance.save()
        return instance

    def get_is_favorited(self, obj):
        if self.context:
            user = self.context['request'].user
            favorites = obj.favorited.all()
            if user.is_authenticated and user in favorites:
                return True
        return False

    def get_is_in_shopping_cart(self, obj):
        cart = obj.in_shopping_cart.all()
        if cart:
            return True
        return False


# Проверить!!!
class FavoriteRecipeSerializer(serializers.ModelSerializer):
    user = AuthorSerializer(read_only=True)
    recipe = RecipeSerializer(read_only=True)
    name = ShortRecipeSerializer(read_only=True)
    image = ShortRecipeSerializer(read_only=True)
    cooking_time = ShortRecipeSerializer(read_only=True)

    class Meta:
        model = FavoriteRecipes
        fields = ('user', 'recipe', 'id', 'name', 'image', 'cooking_time')

    def to_representation(self, instance):
        serializer = ShortRecipeSerializer(instance)
        return serializer.data


class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.StringRelatedField(
        source='author', read_only=True)
    id = serializers.PrimaryKeyRelatedField(
        source='author', read_only=True)
    username = serializers.StringRelatedField(
        source='author', read_only=True)
    first_name = serializers.StringRelatedField(
        source='author', read_only=True)
    last_name = serializers.StringRelatedField(
        source='author', read_only=True)
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField(
        source='author', read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ['email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count'
                  ]

    def get_recipes(self, obj):
        author = get_object_or_404(User, pk=obj.author.id)
        serializer = ShortRecipeSerializer(author.recipes.all(), many=True)
        return serializer.data

    def get_is_subscribed(self, obj):
        if self.context:
            user = self.context.get('request').user
            if obj.user == user:
                return True
        if obj:
            return True
        return False

    def get_recipes_count(self, obj):
        author = obj.author
        recipes = Recipe.objects.filter(author=author)
        return len(recipes)
