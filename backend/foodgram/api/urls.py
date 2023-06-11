from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipes.views import ListTagViewSet, RecipeViewSet, IngredientsViewSet, SubscriptionViewSet

router = DefaultRouter()

router.register('tags', ListTagViewSet)
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientsViewSet)
router.register('ingredients/(?P<id>\d+)', IngredientsViewSet)
router.register('users', SubscriptionViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('users.urls'), name='users'),
]
