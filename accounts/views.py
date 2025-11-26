# backend/accounts/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

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

class OrganizationView(APIView):
    def get(self, request):
        if not request.user.is_super_admin:
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
        if not request.user.is_super_admin:
            return Response({'error': 'Access denied'}, status=403)
        org, _ = Organization.objects.get_or_create()
        for field in ['name', 'contact_email', 'contact_phone', 'timezone']:
            if field in request.data:
                setattr(org, field, request.data[field])
        org.save()
        return Response({'message': 'Organization updated'})