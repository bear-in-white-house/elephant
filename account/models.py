from django.db import models
from django.contrib.auth.models import User

from elephant.utils.utils import PathAndRename


class Permission(models.Model):
    key = models.CharField(max_length=10, unique=True)
    display_name = models.CharField(max_length=20)


class Account(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    is_admin = models.BooleanField(default=False)
    avatar = models.FileField(null=True, upload_to=PathAndRename('account/avatar'))
    permission = models.ManyToManyField(Permission)
    username = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.username
