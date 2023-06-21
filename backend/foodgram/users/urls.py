from django.urls import path, include
from rest_framework.routers import DefaultRouter
from djoser.views import UserViewSet, TokenCreateView, TokenDestroyView

from users.views import PaginatedUserViewSet

router = DefaultRouter()

router.register(r'users/?P(<id>\d+)', UserViewSet, basename='users_profile')
router.register('users', PaginatedUserViewSet, basename='users')

urlpatterns = [
    path('auth/token/login/', TokenCreateView.as_view(), name='create_token'),
    path('', include(router.urls)),
    path(
        'auth/token/logout/',
        TokenDestroyView.as_view(),
        name='destroy_token')
]
