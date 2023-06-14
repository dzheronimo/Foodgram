from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, password=None):
        if username is None:
            raise TypeError('У пользователя должен быть username')

        if email is None:
            raise TypeError('У пользователя должен быть email')

        user = self.model(
            username=username, email=self.normalize_email(email),
            first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password, first_name, last_name):

        if password is None:
            raise TypeError('У суперпользователя должен быть password')

        user = self.create_user(username, email, password, first_name, last_name)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=150, unique=True)
    email = models.EmailField(db_index=True, unique=True, max_length=254)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name
