# backend/hr/urls.py
from django.urls import path
from .views import StaffListView, HrUserCreateView

urlpatterns = [
    path('staff/', StaffListView.as_view(), name='hr-staff-list'),
    path('staff/create/', HrUserCreateView.as_view(), name='hr-user-create'),
]