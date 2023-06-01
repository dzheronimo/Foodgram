from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet

router = DefaultRouter()

# router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('users/', UserViewSet.as_view(), name='users'),
    path('', include(router.urls), name='api')
]