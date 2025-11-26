# backend/accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Organization(models.Model):
    """Single organization per NGO"""
    name = models.CharField(max_length=100, unique=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    timezone = models.CharField(max_length=50, default='Africa/Nairobi')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    """Custom user with Super Admin flag"""
    email = models.EmailField(unique=True)
    is_super_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']