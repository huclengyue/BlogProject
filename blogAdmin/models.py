from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import forms


class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)

    class Meta(AbstractUser.Meta):
        pass
