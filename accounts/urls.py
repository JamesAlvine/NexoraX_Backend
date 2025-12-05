# backend/accounts/urls.py
from django.urls import path
from .views import (
    csrf,
    LoginView,
    MeView,
    UserListView,
    OrganizationView,
    UserCreateView,
    UserDetailView,  # ✅ Must be imported
)

urlpatterns = [
    path('auth/csrf/', csrf, name='csrf'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/me/', MeView.as_view(), name='me'),
    path('users/', UserListView.as_view(), name='users'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),  # ✅ Now defined
    path('organization/', OrganizationView.as_view(), name='organization'),
]