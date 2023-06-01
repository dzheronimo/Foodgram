from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework import permissions
from users.models import User
from users.serializers import UserSerializer


class UserViewSet(ListCreateAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = UserSerializer


    # def create(self, request, *args, **kwargs):

# Create your views here.
