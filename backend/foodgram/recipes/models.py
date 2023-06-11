from django.core.validators import validate_unicode_slug
from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7)
    slug = models.SlugField(max_length=200, validators=[validate_unicode_slug, ])

    class Meta:
        # ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes')
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='media/recipes/images/',
        null=False,
        default=None
    )
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientAmountRecipe', related_name='recipes')
    tags = models.ManyToManyField(Tag, related_name='recipes')
    cooking_time = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)
    is_favorite = models.ManyToManyField(User, through='FavoriteRecipes', related_name='favorites')
    is_in_shopping_cart = models.ManyToManyField(User, through='ShoppingCart', related_name='cart')

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class FavoriteRecipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='in_favorites')

    class Meta:
        verbose_name = 'Избранное'

        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='user_recipe'
            )
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='in_carts')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='user_cart_recipe'
            )
        ]


class IngredientAmountRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='amount_recipe')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='amount_ingredient')
    amount = models.IntegerField()

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'recipe',),
                name='recipe_ingredient'
            )
        ]


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriber')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')

    class Meta:
        verbose_name = 'Подписки'
        ordering = ['author']

        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author', ),
                name='user_author'
            )
        ]
