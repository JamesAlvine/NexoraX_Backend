# backend/crm/urls.py
from django.urls import path
from .views import CrmDashboardView

urlpatterns = [
    path('dashboard/', CrmDashboardView.as_view(), name='crm-dashboard'),
]