# backend/crm/models.py
from django.db import models
from accounts.models import Organization, User

class Donor(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    total_given = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_donation = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Donor: {self.name}"

class Beneficiary(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    needs = models.JSONField(default=list)
    services_received = models.JSONField(default=list)

    def __str__(self):
        return f"Beneficiary: {self.name} ({self.unique_id})"

class Interaction(models.Model):
    INTERACTION_TYPES = [
        ('call', 'Phone Call'),
        ('meeting', 'Meeting'),
        ('email', 'Email'),
        ('note', 'Note'),
    ]
    
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, null=True, blank=True)
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, null=True, blank=True)
    interaction_type = models.CharField(max_length=10, choices=INTERACTION_TYPES)
    notes = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        target = self.donor or self.beneficiary
        return f"{self.get_interaction_type_display()} with {target}"