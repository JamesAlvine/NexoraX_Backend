# backend/volunteers/models.py
from django.db import models
from accounts.models import User

class VolunteerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    skills = models.JSONField(default=list)  # e.g., ["First Aid", "Translation"]
    availability = models.CharField(max_length=100, blank=True)
    department_preferences = models.JSONField(default=list)  # e.g., ["Health", "Education"]
    experience_years = models.PositiveIntegerField(default=0)
    emergency_contact = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Volunteer: {self.user.email}"

# Department definitions (used for matching)
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    required_skills = models.JSONField(default=list)  # e.g., ["First Aid", "Teaching"]

    def __str__(self):
        return self.name