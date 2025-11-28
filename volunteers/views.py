# backend/volunteers/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import VolunteerProfile, Department

User = get_user_model()

class SkillMatrixView(APIView):
    def get(self, request):
        # HR and Super Admin can view
        if not (request.user.is_super_admin or 
                getattr(request.user, 'is_hr', False)):
            return Response({'error': 'Access denied'}, status=403)

        # Fetch volunteers with skills
        volunteers = VolunteerProfile.objects.select_related('user').all()
        departments = Department.objects.all()

        # Calculate role-fit scores
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
        """Smart algorithm for role-fit scoring (0-100)"""
        score = 0
        
        # Skill match (50% weight)
        matched_skills = set(volunteer.skills) & set(department.required_skills)
        if department.required_skills:
            skill_score = (len(matched_skills) / len(department.required_skills)) * 50
            score += skill_score
        
        # Department preference match (30% weight)
        if department.name in volunteer.department_preferences:
            score += 30
        
        # Experience (20% weight)
        if volunteer.experience_years >= 2:
            score += 20
        elif volunteer.experience_years >= 1:
            score += 10
        
        return min(round(score, 1), 100)