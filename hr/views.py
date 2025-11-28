# backend/hr/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from accounts.models import UserAppAssignment

User = get_user_model()

class StaffListView(APIView):
    def get(self, request):
        if not (getattr(request.user, 'is_super_admin', False) or 
                getattr(request.user, 'is_hr', False)):
            return Response({'error': 'HR access required'}, status=403)
        
        staff_ids = UserAppAssignment.objects.filter(
            app__name='HR'
        ).values_list('user_id', flat=True)
        staff = User.objects.filter(id__in=staff_ids).values('id', 'email')
        return Response(list(staff))


# ✅ ADD THIS MISSING VIEW
class LeaveRequestView(APIView):
    def get(self, request):
        # For now, return mock data
        if not (getattr(request.user, 'is_super_admin', False) or 
                getattr(request.user, 'is_hr', False)):
            return Response({'error': 'HR access required'}, status=403)
        return Response([])

    def post(self, request):
        if not (getattr(request.user, 'is_super_admin', False) or 
                getattr(request.user, 'is_hr', False)):
            return Response({'error': 'HR access required'}, status=403)
        return Response({'message': 'Leave request submitted'}, status=201)