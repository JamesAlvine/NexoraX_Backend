# backend/volunteers/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import VolunteerProfile, Department

User = get_user_model()

class SkillMatrixView(APIView):
    def get(self, request):
        if not (getattr(request.user, 'is_super_admin', False) or 
                getattr(request.user, 'is_hr', False)):
            return Response({'error': 'Access denied'}, status=403)

        volunteers = VolunteerProfile.objects.select_related('user').all()
        departments = Department.objects.all()
        matrix = []
        
        for v in volunteers:
            scores = {}
            for dept in departments:
                score = self.calculate_fit_score(v, dept)
                scores[dept.name] = score
            matrix.append({
                'email': v.user.email,
                'skills': v.skills,
                'department_preferences': v.department_preferences,
                'experience_years': v.experience_years,
                'scores': scores,
                'best_fit': max(scores, key=scores.get) if scores else None
            })
        return Response(matrix)

    def calculate_fit_score(self, volunteer, department):
        score = 0
        # Skill match (50%)
        matched = set(volunteer.skills) & set(department.required_skills)
        if department.required_skills:
            score += (len(matched) / len(department.required_skills)) * 50
        # Preference match (30%)
        if department.name in volunteer.department_preferences:
            score += 30
        # Experience (20%)
        if volunteer.experience_years >= 2:
            score += 20
        elif volunteer.experience_years >= 1:
            score += 10
        return min(round(score, 1), 100)