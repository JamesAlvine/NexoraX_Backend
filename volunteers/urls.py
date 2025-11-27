# backend/volunteers/urls.py
from django.urls import path
from .views import VolunteerListView, HourLogListView

urlpatterns = [
    path('volunteers/', VolunteerListView.as_view()),
    path('hour-logs/', HourLogListView.as_view()),  # ✅ NEW
]