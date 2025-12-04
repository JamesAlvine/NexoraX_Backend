# backend/accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator


# ============================
# CORE MODELS
# ============================

class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    timezone = models.CharField(max_length=50, default='Africa/Nairobi')

    def __str__(self):
        return self.name


class App(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# ============================
# CUSTOM USER MODEL
# ============================

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_super_admin = models.BooleanField(default=False)
    # Optional: link to organization
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Keep for compatibility

    def __str__(self):
        return self.email


# ============================
# RELATIONAL MODELS
# ============================

class UserAppAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='app_assignments')
    app = models.ForeignKey(App, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'app')

    def __str__(self):
        return f"{self.user.email} → {self.app.name}"