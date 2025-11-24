# backend/accounts/serializers.py
from rest_framework import serializers
from .models import User, Organization

class UserListSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'is_super_admin', 'organization_name']