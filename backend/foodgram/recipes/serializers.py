import base64

from django.core.files.base import ContentFile
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Count, Max, F
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


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)

class IngredientSerializer(serializers.ModelSerializer):
    # amount = serializers.SerializerMethodField()
    # amount = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.annotate(amount=Max('amount_ingredient__amount')))
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class IngredientAmountRecipeSerializer(serializers.ModelSerializer):
    # id = IngredientSerializer(many=True)
    # name = IngredientSerializer(many=True)
    # measurement_unit = IngredientSerializer(many=True)
    id = serializers.IntegerField()
    name = serializers.CharField()
    measurement_unit = serializers.CharField()
    # amount = serializers.PrimaryKeyRelatedField(source='recipe', queryset=Recipe.objects.all())

    def get_amount(self, obj):
        recipe = obj.recipes3
        return obj

    class Meta:
        model = IngredientAmountRecipe
        fields = ['id', 'name', 'measurement_unit']


class RecipeSerializer(serializers.ModelSerializer):
    tags = ListTagSerializer(many=True, read_only=True)
    author = AuthorSerializer(read_only=True)
    ingredients = IngredientAmountRecipeSerializer(many=True, read_only=True)
    # ingredients = IngredientAmountRecipeSerializer(source='ingredientamountrecipe_set', many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time']

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')

        if not ingredients:
            raise serializers.ValidationError(
                {"ingredients": "Для рецепта требуется минимум один ингредиент"}
            )
        for ingredient in ingredients:
            if not Ingredient.objects.filter(pk=ingredient.get('id')):
                raise serializers.ValidationError(
                    {"ingreients": "Можно выбрать только "
                                  "существующий ингредиент!"}
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
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        instance.image = validated_data.get('image', instance.image)

        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            instance.tags.set(tags_data)
        if 'ingredients' in validated_data:
            IngredientAmountRecipe.objects.filter(recipe=instance).delete()
            ingredients_data = validated_data.pop('ingredients')
            for ingredient in ingredients_data:
                ingredient_instance = get_object_or_404(Ingredient, pk=ingredient.get('id'))
                if ingredient_instance:
                    IngredientAmountRecipe.objects.create(
                        recipe=instance,
                        ingredient=ingredient_instance,
                        amount=ingredient.get('amount')
                    )

        instance.save()
        return instance

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
