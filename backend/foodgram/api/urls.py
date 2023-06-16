from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipes.views import ListTagViewSet, RecipeViewSet, IngredientsViewSet

app_name = 'api'

router = DefaultRouter()

router.register('tags', ListTagViewSet)
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientsViewSet)


urlpatterns = [
    path('', include('users.urls'), name='users'),

    path('', include(router.urls)),
]
