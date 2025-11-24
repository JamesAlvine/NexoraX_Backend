# backend/volunteers/models.py
from django.db import models  # ✅ MUST import models
from accounts.models import User

class VolunteerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.JSONField(default=list)
    availability = models.CharField(max_length=100, blank=True)
    hours_contributed = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Volunteer: {self.user.email}"