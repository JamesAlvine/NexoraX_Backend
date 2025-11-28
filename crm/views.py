# backend/crm/views.py
from rest_framework.views import APIView
from rest_framework.response import Response

class CrmDashboardView(APIView):
    """Return CRM dashboard stats (mock data for now)."""
    def get(self, request):
        if not getattr(request.user, 'is_super_admin', False):
            return Response({'error': 'Access denied'}, status=403)
        return Response({
            'donors': 120,
            'beneficiaries': 340,
            'interactions': 89,
            'active_campaigns': 3
        })