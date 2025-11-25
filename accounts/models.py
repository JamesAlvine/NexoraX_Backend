# backend/accounts/models.py
from django.db import models 
from django.contrib.auth.models import AbstractUser

class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    #logo = models.ImageField(upload_to='org_logos/', blank=True, null=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    timezone = models.CharField(max_length=50, default='Africa/Nairobi')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class App(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class UserRole(models.Model):
    name = models.CharField(max_length=100)
    app = models.ForeignKey(App, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'app')

    def __str__(self):
        return f"{self.name} ({self.app.name})"

class UserAppAssignment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='assignments')
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'app')

    def __str__(self):
        return f"{self.user.email} → {self.app.name}"

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_super_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']