# backend/accounts/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import UserAppAssignment, App

User = get_user_model()

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
            'is_super_admin': getattr(user, 'is_super_admin', False)
        })

class UserListView(APIView):
    def get(self, request):
        if not request.user.is_super_admin:
            return Response({'error': 'Access denied'}, status=403)
        users = User.objects.values('id', 'username', 'email')
        return Response(list(users))

class UserAssignmentView(APIView):
    def post(self, request):
        if not request.user.is_super_admin:
            return Response({'error': 'Access denied'}, status=403)
        user_id = request.data.get('user_id')
        app_name = request.data.get('app_name')
        try:
            user = User.objects.get(id=user_id)
            app = App.objects.get(name=app_name)
            UserAppAssignment.objects.update_or_create(
                user=user,
                app=app,
                defaults={'role': None}
            )
            return Response({'message': 'Assignment saved'})
        except (User.DoesNotExist, App.DoesNotExist):
            return Response({'error': 'Invalid user or app'}, status=400)

class OrganizationView(APIView):
    def get(self, request):
        if not request.user.is_super_admin:
            return Response({'error': 'Access denied'}, status=403)
        org = Organization.objects.first()
        return Response({
            'id': org.id,
            'name': org.name,
            'contact_email': org.contact_email,
            'contact_phone': org.contact_phone,
            'timezone': org.timezone
        })

    def post(self, request):
        if not request.user.is_super_admin:
            return Response({'error': 'Access denied'}, status=403)
        org = Organization.objects.first()
        org.name = request.data.get('name', org.name)
        org.contact_email = request.data.get('contact_email', org.contact_email)
        org.contact_phone = request.data.get('contact_phone', org.contact_phone)
        org.timezone = request.data.get('timezone', org.timezone)
        org.save()
        return Response({'message': 'Organization updated'})