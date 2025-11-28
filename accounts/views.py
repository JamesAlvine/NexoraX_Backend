# backend/accounts/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Organization  # ✅ Import your model

User = get_user_model()

@require_GET
@ensure_csrf_cookie
def csrf(request):
    """Set CSRF cookie for Angular frontend."""
    return JsonResponse({'detail': 'CSRF cookie set'})

class LoginView(APIView):
    """Handle user login with email/password."""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        password = request.data.get('password', '')

        if not email or not password:
            return Response({'error': 'Email and password required.'}, status=400)

        user = authenticate(request, username=email, password=password)
        if not user:
            return Response({'error': 'Invalid email or password.'}, status=401)

        login(request, user)
        return Response({
            'id': user.id,
            'email': user.email,
            'is_super_admin': getattr(user, 'is_super_admin', False)
        })

class MeView(APIView):
    """Return current user profile."""
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Not authenticated'}, status=401)
        return Response({
            'id': request.user.id,
            'email': request.user.email,
            'is_super_admin': getattr(request.user, 'is_super_admin', False)
        })

class UserListView(APIView):
    """List all users (Super Admin only)."""
    def get(self, request):
        if not getattr(request.user, 'is_super_admin', False):
            return Response({'error': 'Access denied'}, status=403)
        users = User.objects.only('id', 'email', 'is_super_admin').order_by('email')
        data = [
            {'id': u.id, 'email': u.email, 'is_super_admin': u.is_super_admin}
            for u in users
        ]
        return Response(data)

class OrganizationView(APIView):
    """Get or update organization settings."""
    def get(self, request):
        if not getattr(request.user, 'is_super_admin', False):
            return Response({'error': 'Access denied'}, status=403)
        org, _ = Organization.objects.get_or_create(
            defaults={'name': 'Neos NGO', 'contact_email': 'admin@nexorax.org'}
        )
        return Response({
            'id': org.id,
            'name': org.name,
            'contact_email': org.contact_email,
            'contact_phone': org.contact_phone,
            'timezone': org.timezone
        })

    def post(self, request):
        if not getattr(request.user, 'is_super_admin', False):
            return Response({'error': 'Access denied'}, status=403)
        org, _ = Organization.objects.get_or_create()
        for field in ['name', 'contact_email', 'contact_phone', 'timezone']:
            if field in request.data:
                setattr(org, field, request.data[field])
        org.save()
        return Response({'message': 'Organization updated'})