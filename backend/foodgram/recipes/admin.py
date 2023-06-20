from django.contrib import admin

from .models import (
    Tag, Recipe, Ingredient,
    IngredientAmountRecipe, FavoriteRecipes,
    ShoppingCart, Subscription
)


class IngredientAmountRecipeInline(admin.TabularInline):
    model = IngredientAmountRecipe
    extra = 1


class FavoriteRecipesInline(admin.TabularInline):
    model = FavoriteRecipes
    fk_name = ''
    extra = 1


class ShoppingCartInline(admin.TabularInline):
    model = ShoppingCart
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_filter = ('name', 'author', )
    list_display = ('name', 'author', )
    list_display_links = ('name', 'author', )
    inlines = [FavoriteRecipesInline,
               IngredientAmountRecipeInline,
               ShoppingCartInline,
               ]

    readonly_fields = ('id', 'favorited_count', )
    # fieldsets = (
    #     ('Дополнительная информация', {
    #         'fields': ('favorited_count',),
    #     }),
    #
    # )

    def favorited_count(self, obj):
        return FavoriteRecipes.objects.filter(recipe=obj).count()

    favorited_count.short_description = 'Пользователи добавили в избранное'


class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name', )
    list_display = ('name', 'measurement_unit', )
    list_display_links = ('name', 'measurement_unit', )


admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(FavoriteRecipes)
admin.site.register(ShoppingCart)
