# backend/accounts/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Organization, App, UserAppAssignment

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
        return Response([
            {'id': u.id, 'email': u.email, 'is_super_admin': u.is_super_admin}
            for u in users
        ])

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

class UserCreateView(APIView):
    """Create a new user (Super Admin only)."""
    def post(self, request):
        # ✅ Ensure user is authenticated AND super admin
        if not (request.user.is_authenticated and getattr(request.user, 'is_super_admin', False)):
            return Response({'error': 'Access denied'}, status=403)

        email = request.data.get('email', '').strip().lower()
        password = request.data.get('password', '')
        is_super_admin = request.data.get('is_super_admin', False)
        apps = request.data.get('apps', [])

        if not email or not password:
            return Response({'error': 'Email and password required'}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'User already exists'}, status=400)

        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )
        user.is_super_admin = is_super_admin
        user.save()

        # Assign apps
        for app_name in apps:
            try:
                app = App.objects.get(name=app_name)
                UserAppAssignment.objects.create(user=user, app=app)
            except App.DoesNotExist:
                continue

        return Response({
            'id': user.id,
            'email': user.email,
            'is_super_admin': user.is_super_admin
        }, status=201)