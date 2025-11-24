# backend/hr/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import StaffProfile

User = get_user_model()

class StaffListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_super_admin:
            return Response({'error': 'Access denied'}, status=403)
        staff = StaffProfile.objects.select_related('user').values(
            'user__email', 'department', 'position'
        )
        return Response(list(staff))