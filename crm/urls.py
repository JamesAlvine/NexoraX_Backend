# backend/crm/urls.py
from django.urls import path
from .views import CrmDashboardView  # ✅ Now importable

urlpatterns = [
    path('dashboard/', CrmDashboardView.as_view(), name='crm_dashboard'),
]