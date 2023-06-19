from django.contrib import admin

from .models import User
from recipes.models import FavoriteRecipes, Subscription, ShoppingCart


class ShoppingCartInline(admin.TabularInline):
    model = ShoppingCart
    extra = 1


class FavoritesInline(admin.TabularInline):
    model = FavoriteRecipes
    extra = 1


class SubscriptionsInline(admin.StackedInline):
    model = Subscription
    fk_name = 'user'
    extra = 1


class UserAdmin(admin.ModelAdmin):
    list_filter = ('username', 'email', )
    list_display = ('username', 'email', 'last_name', 'first_name', )
    list_display_links = ('username', 'email', 'last_name', 'first_name', )
    inlines = [FavoritesInline, ShoppingCartInline, SubscriptionsInline]


admin.site.register(User, UserAdmin)
admin.site.register(Subscription)

