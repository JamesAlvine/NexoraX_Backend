# backend/accounts/urls.py
from django.urls import path
from .views import csrf, LoginView, UserListView, OrganizationView

urlpatterns = [
    path('auth/csrf/', csrf),
    path('auth/login/', LoginView.as_view()),
    path('super/users/', UserListView.as_view()),    
    path('super/organization/', OrganizationView.as_view()),
]