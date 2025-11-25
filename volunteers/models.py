# backend/volunteers/models.py
from django.db import models
from accounts.models import User

class VolunteerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    skills = models.JSONField(default=list)  # e.g., ["Teaching", "Translation"]
    availability = models.CharField(max_length=100, blank=True)  # e.g., "Weekends"
    hours_contributed = models.PositiveIntegerField(default=0)
    emergency_contact = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Volunteer: {self.user.email}"