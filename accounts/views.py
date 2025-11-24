# backend/accounts/views.py
from django.db import transaction
from .models import User
from hr.models import StaffProfile
from volunteers.models import VolunteerProfile

class UserCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_super_admin:
            return Response({'error': 'Access denied'}, status=403)

        email = request.data.get('email')
        password = request.data.get('password', 'TempPass123!')
        user_type = request.data.get('user_type')  # 'staff' or 'volunteer'
        extra_data = request.data.get('extra_data', {})

        if User.objects.filter(email=email).exists():
            return Response({'error': 'User already exists'}, status=400)

        with transaction.atomic():
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )

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
                    availability=extra_data.get('availability', '')
                )

        return Response({'id': user.id, 'email': user.email}, status=201)