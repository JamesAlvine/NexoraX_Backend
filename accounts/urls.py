# backend/accounts/urls.py
from django.urls import path
from .views import (
    csrf,           # ✅ Function-based view
    LoginView,      # ✅ Class-based view
    MeView,
    UserListView,
    OrganizationView,
    UserCreateView
)

urlpatterns = [
    path('auth/csrf/', csrf, name='csrf'),          # ✅ No .as_view()
    path('auth/login/', LoginView.as_view(), name='login'),   # ✅ WITH .as_view()
    path('auth/me/', MeView.as_view(), name='me'),
    path('users/', UserListView.as_view(), name='users'),
    path('organization/', OrganizationView.as_view(), name='organization'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
]