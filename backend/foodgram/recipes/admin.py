from django.contrib import admin

from .models import Tag, Recipe, Ingredient, IngredientAmountRecipe, FavoriteRecipes


class IngredientAmountRecipeInline(admin.TabularInline):
    model = IngredientAmountRecipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientAmountRecipeInline]


admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
