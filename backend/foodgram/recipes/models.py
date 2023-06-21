from django.core.validators import validate_unicode_slug, MinValueValidator
from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7)
    slug = models.SlugField(
        max_length=200, validators=[validate_unicode_slug, ])

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Ингредиент', max_length=200)
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
        upload_to='recipes',
        null=False,
        default=None
    )
    text = models.TextField()
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientAmountRecipe',
                                         blank=False,
                                         related_name='recipes',
                                         verbose_name='Ингредиенты')
    tags = models.ManyToManyField(Tag, related_name='recipes')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(limit_value=1),
                    ])
    pub_date = models.DateTimeField(auto_now_add=True)
    favorited = models.ManyToManyField(
        User, through='FavoriteRecipes', related_name='favorites')
    in_shopping_cart = models.ManyToManyField(User,
                                              through='ShoppingCart',
                                              related_name='cart')

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class FavoriteRecipes(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='in_favorites')

    class Meta:
        verbose_name = 'Избранное'

        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='user_recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe} в избранном'


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='in_carts')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзины покупок'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='user_cart_recipe'
            )
        ]

    def __str__(self):
        return f'Корзина {self.user.username}'


class IngredientAmountRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name='amount_recipe',
                                   verbose_name='Ингредиент')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='amount_ingredient')
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(limit_value=1), ])

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
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='subscriber',
                             verbose_name='Подписчик')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='subscriptions',
                               verbose_name='Автор')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

        ordering = ['author']

        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author', ),
                name='user_author'
            )
        ]

    def __str__(self):
        return f'{self.user.username} is following {self.author.username}'
