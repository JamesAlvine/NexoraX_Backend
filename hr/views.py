# backend/hr/views.py
import secrets
import string
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import UserAppAssignment, App, Organization

User = get_user_model()

def generate_temporary_password(length=12):
    """Generate secure temporary password for new users"""
    alphabet = string.ascii_letters + string.digits + "!@#$%&"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

class StaffListView(APIView):
    """
    List HR staff.
    - HR users: see only HR staff
    - Super Admin: see all users (but this route is HR-focused)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Verify HR access via app assignment
        is_hr = UserAppAssignment.objects.filter(
            user=request.user,
            app__name='HR'
        ).exists()

        if not (request.user.is_super_admin or is_hr):
            return Response({'error': 'HR access required'}, status=403)

        # HR sees only HR staff; Super Admin *can* see all here but typically uses /users/
        if is_hr:
            staff_ids = UserAppAssignment.objects.filter(
                app__name='HR'
            ).values_list('user_id', flat=True)
            staff = User.objects.filter(id__in=staff_ids).values(
                'id', 'email', 'is_active', 'date_joined'
            )
        else:
            # Super Admin sees all
            staff = User.objects.values(
                'id', 'email', 'is_active', 'date_joined'
            )

        return Response(list(staff))

class HrUserCreateView(APIView):
    """
    HR can create new HR staff only.
    - Auto-generates password
    - Assigns user to 'HR' app
    - Sets must_change_password = True
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Only HR (via app assignment) can create
        is_hr = UserAppAssignment.objects.filter(
            user=request.user,
            app__name='HR'
        ).exists()

        if not is_hr:
            return Response({'error': 'HR access required'}, status=403)

        email = request.data.get('email', '').strip().lower()
        if not email:
            return Response({'error': 'Email is required'}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'User already exists'}, status=400)

        # Generate temporary password
        temp_password = generate_temporary_password()

        # Use default org
        org, _ = Organization.objects.get_or_create(
            name='Neos NGO',
            defaults={'contact_email': 'admin@nexorax.org'}
        )

        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=temp_password,
            organization=org,
            must_change_password=True
        )

        # Assign to HR app only
        hr_app, _ = App.objects.get_or_create(name='HR')
        UserAppAssignment.objects.create(user=user, app=hr_app)

        return Response({
            'message': 'HR staff created successfully',
            'email': user.email
            # Do NOT return password to HR — only Super Admin sees it
        }, status=201)