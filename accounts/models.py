# backend/accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser  # ✅ MUST import this

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_super_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']