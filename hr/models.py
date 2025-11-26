# backend/hr/models.py
from django.db import models
from accounts.models import User

class StaffProfile(models.Model):
    """HR staff profile (only for is_staff=True users)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    department = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    hire_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Staff: {self.user.email}"