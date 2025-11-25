# backend/hr/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from accounts.models import UserAppAssignment

User = get_user_model()

class StaffListView(APIView):
    def get(self, request):
        if not request.user.is_super_admin:
            return Response({'error': 'Access denied'}, status=403)
        staff_ids = UserAppAssignment.objects.filter(
            app__name='HR'
        ).values_list('user_id', flat=True)
        staff = User.objects.filter(id__in=staff_ids).values('id', 'username', 'email')
        return Response(list(staff))