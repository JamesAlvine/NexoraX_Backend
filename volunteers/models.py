# backend/volunteers/models.py
from django.db import models
from accounts.models import User

class VolunteerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    skills = models.JSONField(default=list)
    availability = models.CharField(max_length=100, blank=True)
    hours_contributed = models.PositiveIntegerField(default=0)
    emergency_contact = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Volunteer: {self.user.email}"

# ✅ NEW: Hour Log
class HourLog(models.Model):
    volunteer = models.ForeignKey(VolunteerProfile, on_delete=models.CASCADE, related_name='hour_logs')
    date = models.DateField()
    hours = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 2.5 hours
    project = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.volunteer.user.email} - {self.hours}h on {self.date}"