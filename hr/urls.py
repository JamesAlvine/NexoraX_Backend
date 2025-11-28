# backend/hr/urls.py
from django.urls import path
from .views import StaffListView, LeaveRequestView

urlpatterns = [
    path('staff/', StaffListView.as_view()),
    path('leave/', LeaveRequestView.as_view()),
]