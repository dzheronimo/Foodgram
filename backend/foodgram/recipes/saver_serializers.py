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
    # id = serializers.StringRelatedField()
    # id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    # id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    # name = serializers.CharField()
    # amount = serializers.IntegerField(source='amount_ingredient.amount')

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class IngredientDetailSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    ingredient = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientAmountRecipe
        fields = ['id', 'ingredient', 'measurement_unit', 'amount', ]


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientDetailSerializer(source="ingredientamountrecipe_set", many=True)

    class Meta:
        model = Recipe
        fields = ['name', 'ingredients']
        depth = 1


class IngredientAmountRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    # id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    # amount = serializers.IntegerField()
    # id = serializers.PrimaryKeyRelatedField(source='ingredient.id', queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientAmountRecipe
        fields = ['id', 'amount']

    def create(self, validated_data):
        ingredient_id = validated_data.pop('id')
        amount = IngredientAmountRecipe.objects.create(**validated_data)
        amount.id.set(ingredient_id)
        return amount


class RecipeCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    ingredients = IngredientAmountRecipeSerializer(source='ingredientamountrecipe_set', many=True)

    class Meta:
        model = Recipe
        fields = ['ingredients', 'tags', 'name', 'text', 'cooking_time']

    def to_representation(self, instance):
        serializer = RecipeListRetrieveSerializer(instance)
        return serializer.data


    def create(self, validated_data):
        tags = validated_data.pop('tags')
        print(validated_data)
        # ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)

        recipe.tags.set(tags)
        # recipe.ingredients.set(ingredients)


        return recipe

    # def create(self, validated_data):
    #     ingredients = validated_data.pop('ingredients')
    #     tags = validated_data.pop('tags')
    #     recipe = Recipe.objects.create(**validated_data)
    #     recipe.tags.set(tags)
    #     print(ingredients)
    #     for ingredient in ingredients:
    #         exists_ingredient = ingredient['id']
    #         print(exists_ingredient)
    #         current_ingredient = get_object_or_404(Ingredient, id=exists_ingredient.id)
    #         # current_ingredient.save()
    #         IngredientAmountRecipe.objects.create(
    #             recipe=recipe, ingredient=current_ingredient, amount=ingredient['amount']
    #         )
    #     return recipe


class ListIngredientAmountRecipeSerializer(serializers.ModelSerializer):
    id = IngredientSerializer()
    # id = serializers.ReadOnlyField(source='ingredient.id')
    # id = serializers.RelatedField(queryset=Ingredient.objects.all())  # --- На крайний случай
    # id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    # name = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    # measurement_unit = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = IngredientSerializer(many=True)
    measurement_unit = IngredientSerializer(many=True)
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientAmountRecipe
        fields = ['id', 'name', 'measurement_unit', 'amount']


class RecipeListRetrieveSerializer(serializers.ModelSerializer):
    tags = ListTagSerializer(many=True)
    ingredients = RecipeSerializer(many=True)
    # # ingredients = IngredientAmountRecipeSerializer(
    # #     source='ingredientamountrecipe_set', many=True)
    author = AuthorSerializer()

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients', 'name',
                  'text', 'cooking_time']
