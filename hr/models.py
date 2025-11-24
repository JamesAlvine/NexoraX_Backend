# backend/hr/models.py
from django.db import models  # ✅ MUST import models
from accounts.models import User

class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    def __str__(self):
        return f"Staff: {self.user.email}"