# backend/volunteers/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import VolunteerProfile

User = get_user_model()

class VolunteerListView(APIView):
    """List all volunteers with skills, availability, and hours."""
    def get(self, request):
        if not request.user.is_superuser:
            return Response({'error': 'Access denied'}, status=403)
        volunteers = VolunteerProfile.objects.select_related('user').values(
            'user__email',
            'skills',
            'availability',
            'hours_contributed'
        )
        return Response(list(volunteers))

class HourLogListView(APIView):
    """List and create hour logs."""
    def get(self, request):
        if not request.user.is_superuser:
            return Response({'error': 'Access denied'}, status=403)
        # Implement later
        return Response([])

    def post(self, request):
        if not request.user.is_superuser:
            return Response({'error': 'Access denied'}, status=403)
        # Implement later
        return Response({'message': 'Hour logged'}, status=201)