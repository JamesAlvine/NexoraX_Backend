# backend/accounts/views.py
import secrets
import string
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, get_user_model, update_session_auth_hash
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Organization, App, UserAppAssignment, User

def generate_temporary_password(length=12):
    """Generate secure temporary password for new users"""
    alphabet = string.ascii_letters + string.digits + "!@#$%&"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

@require_GET
@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({'detail': 'CSRF cookie set'})

class LoginView(APIView):
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
            'is_super_admin': getattr(user, 'is_super_admin', False),
            'must_change_password': getattr(user, 'must_change_password', False),
            'organization': user.organization.name if user.organization else None
        })

class MeView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Not authenticated'}, status=401)
        return Response({
            'id': request.user.id,
            'email': request.user.email,
            'is_super_admin': getattr(request.user, 'is_super_admin', False),
            'must_change_password': getattr(request.user, 'must_change_password', False),
            'organization': request.user.organization.name if request.user.organization else None
        })

class UserListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # HR can only see HR staff; Super Admin sees all
        is_hr = UserAppAssignment.objects.filter(
            user=request.user, 
            app__name='HR'
        ).exists()
        
        if not (request.user.is_super_admin or is_hr):
            return Response({'error': 'HR access required'}, status=403)

        if request.user.is_super_admin:
            staff_ids = User.objects.values_list('id', flat=True)
        else:
            staff_ids = UserAppAssignment.objects.filter(
                app__name='HR'
            ).values_list('user_id', flat=True)

        users = User.objects.filter(id__in=staff_ids).select_related('organization').only(
            'id', 'email', 'is_super_admin', 'is_active', 'organization__name'
        ).order_by('email')
        
        return Response([
            {
                'id': u.id,
                'email': u.email,
                'is_super_admin': u.is_super_admin,
                'is_active': u.is_active,
                'organization': u.organization.name if u.organization else 'Neos NGO'
            }
            for u in users
        ])

class OrganizationView(APIView):
    def get(self, request):
        if not request.user.is_super_admin:
            return Response({'error': 'Super Admin access required'}, status=403)
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
        if not request.user.is_super_admin:
            return Response({'error': 'Super Admin access required'}, status=403)
        org, _ = Organization.objects.get_or_create()
        for field in ['name', 'contact_email', 'contact_phone', 'timezone']:
            if field in request.data:
                setattr(org, field, request.data[field])
        org.save()
        return Response({'message': 'Organization updated'})

# HR: Can only create HR staff
class HrUserCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Verify HR access
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

        # Assign to HR app
        hr_app, _ = App.objects.get_or_create(name='HR')
        UserAppAssignment.objects.create(user=user, app=hr_app)

        return Response({
            'message': 'User created successfully',
            'email': user.email
        }, status=201)

# Super Admin: Full CRUD
class SuperUserCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        if not request.user.is_super_admin:
            return Response({'error': 'Super Admin access required'}, status=403)

        email = request.data.get('email', '').strip().lower()
        department = request.data.get('department', 'HR')
        is_super_admin = request.data.get('is_super_admin', False)

        if not email:
            return Response({'error': 'Email required'}, status=400)
        if User.objects.filter(email=email).exists():
            return Response({'error': 'User exists'}, status=400)

        temp_password = generate_temporary_password()
        org, _ = Organization.objects.get_or_create(
            name='Neos NGO',
            defaults={'contact_email': 'admin@nexorax.org'}
        )

        user = User.objects.create_user(
            username=email,
            email=email,
            password=temp_password,
            is_super_admin=is_super_admin,
            organization=org,
            must_change_password=True
        )

        app, _ = App.objects.get_or_create(name=department)
        UserAppAssignment.objects.create(user=user, app=app)

        return Response({
            'id': user.id,
            'email': user.email,
            'temporary_password': temp_password  # Only Super Admin sees this
        }, status=201)

class UserManageView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404

    def put(self, request, user_id):
        if not request.user.is_super_admin:
            return Response({'error': 'Super Admin access required'}, status=403)
        
        user = self.get_user(user_id)
        data = request.data

        user.is_active = data.get('is_active', user.is_active)
        user.is_super_admin = data.get('is_super_admin', user.is_super_admin)
        user.save()
        return Response({'message': 'User updated'})

    def delete(self, request, user_id):
        if not request.user.is_super_admin:
            return Response({'error': 'Super Admin access required'}, status=403)
        
        user = self.get_user(user_id)
        user.delete()
        return Response({'message': 'User deleted'})

    def post(self, request, user_id):
        if not request.user.is_super_admin:
            return Response({'error': 'Super Admin access required'}, status=403)
        
        user = self.get_user(user_id)
        action = request.data.get('action')

        if action == 'reset_password':
            new_pass = generate_temporary_password()
            user.set_password(new_pass)
            user.must_change_password = True
            user.save()
            return Response({'temporary_password': new_pass})

        elif action == 'reset_2fa':
            # Placeholder for 2FA reset (implement if using 2FA)
            return Response({'message': '2FA reset successfully'})

        return Response({'error': 'Invalid action'}, status=400)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return Response({'error': 'Both passwords required'}, status=400)
            
        if not request.user.check_password(old_password):
            return Response({'error': 'Current password is incorrect'}, status=400)
            
        request.user.set_password(new_password)
        request.user.must_change_password = False
        request.user.save()
        update_session_auth_hash(request, request.user)
        return Response({'message': 'Password updated successfully'})