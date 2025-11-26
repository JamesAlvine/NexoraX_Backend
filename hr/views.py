# backend/hr/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

class StaffListView(APIView):
    def get(self, request):
        if not request.user.is_super_admin:
            return Response({'error': 'Access denied'}, status=403)
        # Show only users with is_staff=True (HR staff)
        staff = User.objects.filter(is_staff=True).values('id', 'username', 'email')
        return Response(list(staff))