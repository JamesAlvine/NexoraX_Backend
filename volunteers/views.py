# backend/volunteers/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import VolunteerProfile

User = get_user_model()

class VolunteerListView(APIView):
    def get(self, request):
        if not request.user.is_super_admin:
            return Response({'error': 'Access denied'}, status=403)
        volunteers = VolunteerProfile.objects.select_related('user').values(
            'user__email',
            'skills',
            'availability',
            'hours_contributed'
        )
        return Response(list(volunteers))