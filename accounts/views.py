# backend/accounts/views.py
"""
Authentication and user management views for Super Admin.
- Login with email/password
- CSRF protection
- Create staff/volunteer users with profiles
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from hr.models import StaffProfile
from volunteers.models import VolunteerProfile

User = get_user_model()


# ============================
# AUTHENTICATION
# ============================

@require_GET
@ensure_csrf_cookie
def csrf(request):
    """Set CSRF cookie for Angular frontend."""
    return JsonResponse({'detail': 'CSRF cookie set'})


class LoginView(APIView):
    """Authenticate user and start session."""
    permission_classes = []

    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        password = request.data.get('password', '')

        if not email or not password:
            return Response({'error': 'Email and password required.'}, status=400)

        # Authenticate by email (username = email)
        user = authenticate(request, username=email, password=password)
        if not user:
            return Response({'error': 'Invalid email or password.'}, status=401)

        login(request, user)
        return Response({
            'id': user.id,
            'email': user.email,
            'is_super_admin': user.is_super_admin
        })


# ============================
# USER CREATION (SUPER ADMIN ONLY)
# ============================

class UserCreateView(APIView):
    """Create a new user (staff or volunteer) with associated profile."""
    
    def post(self, request):
        # Enforce Super Admin access
        if not request.user.is_superuser:
            return Response({'error': 'Access denied'}, status=403)

        email = request.data.get('email', '').strip().lower()
        password = request.data.get('password', 'TempPass123!')
        user_type = request.data.get('user_type')  # 'staff' or 'volunteer'
        extra_data = request.data.get('extra_data', {})

        if not email:
            return Response({'error': 'Email is required'}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists'}, status=400)

        if user_type not in ['staff', 'volunteer']:
            return Response({'error': 'Invalid user_type. Must be "staff" or "volunteer".'}, status=400)

        try:
            with transaction.atomic():
                # Create user
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    is_superuser=False
                )

                # Create profile based on type
                if user_type == 'staff':
                    StaffProfile.objects.create(
                        user=user,
                        department=extra_data.get('department', ''),
                        position=extra_data.get('position', '')
                    )
                elif user_type == 'volunteer':
                    VolunteerProfile.objects.create(
                        user=user,
                        skills=extra_data.get('skills', []),
                        availability=extra_data.get('availability', ''),
                        hours_contributed=0
                    )

                return Response({
                    'id': user.id,
                    'email': user.email,
                    'user_type': user_type
                }, status=201)

        except Exception as e:
            return Response({'error': str(e)}, status=400)