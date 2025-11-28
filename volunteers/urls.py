# backend/volunteers/urls.py
from django.urls import path
from .views import SkillMatrixView

urlpatterns = [
    path('skill-matrix/', SkillMatrixView.as_view(), name='skill_matrix'),
]