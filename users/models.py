from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from users.managers import UserManager


class User(AbstractUser):
    username = models.CharField(max_length=128, unique=True)
    first_name = None
    last_name = None

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access_token": str(refresh.access_token)
        }
