from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    about = models.TextField(max_length=1000, blank=True)

    class Meta:
        ordering = ('id',)
