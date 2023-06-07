from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'last_name', 'first_name')
