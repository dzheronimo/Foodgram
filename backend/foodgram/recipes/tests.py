from django.shortcuts import get_object_or_404
from rest_framework import serializers
from pytils.translit import slugify

from .models import Tag, Ingredient, Recipe, IngredientAmountRecipe
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


class TagSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all())

    class Meta:
        model = Tag
        fields = ['id']


class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    # id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    # amount = serializers.IntegerField(source='amount_ingredient.amount')

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement', 'amount']


class IngredientAmountRecipeSerializer(serializers.ModelSerializer):
    # id = IngredientSerializer()
    # id = serializers.PrimaryKeyRelatedField(queryset=IngredientAmountRecipe.objects.all())
    # amount = serializers.IntegerField()
    id = serializers.PrimaryKeyRelatedField(source='ingredient.id', queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientAmountRecipe
        fields = ['id', 'amount']


# class RecipeCreateSerializer(serializers.ModelSerializer):
#     ingredients = IngredientAmountRecipeSerializer(
#          source='ingredientamountrecipe_set', many=True)
#
#     class Meta:
#         model = Recipe
#         fields = ['ingredients',
#                   'name', 'text', 'cooking_time']
#
#     def validated_data(self):
#         ingredients = self.initial_data['ingredients']
#         return ingredients
#
#     # def create(self, validated_data):
#     #
#     #     return Recipe(**validated_data)


class RecipeCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    ingredients = IngredientAmountRecipeSerializer(many=True, read_only=False, required=True)

    class Meta:
        model = Recipe
        fields = ['ingredients', 'tags', 'name', 'text', 'cooking_time']

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        print(ingredients)
        for ingredient in ingredients:
            current_ingredient = get_object_or_404(Ingredient, id=ingredient['id'])
            # current_ingredient.save()
            IngredientAmountRecipe.objects.create(
                recipe=recipe, ingredient=current_ingredient, amount=ingredient['amount']
            )
        return recipe


class RecipeListRetriveSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = IngredientAmountRecipeSerializer(many=True, read_only=False, required=True)
    # ingredients = IngredientAmountRecipeSerializer(
    #     source='ingredientamountrecipe_set', many=True)
    author = AuthorSerializer()

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients', 'name',
                  'text', 'cooking_time']
