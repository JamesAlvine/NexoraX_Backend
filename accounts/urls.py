# backend/accounts/urls.py
from django.urls import path
from .views import (
    csrf,
    LoginView,
    MeView,
    UserListView,
    OrganizationView,

    SuperUserCreateView,     # was: UserCreateView
    UserManageView,          # for edit/delete
    HrUserCreateView         # for HR create
)

urlpatterns = [
    path('auth/csrf/', csrf, name='csrf'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/me/', MeView.as_view(), name='me'),
    
    # User Management (Super Admin)
    path('users/', UserListView.as_view(), name='user-list'),
    path('super/users/create/', SuperUserCreateView.as_view(), name='super-user-create'),
    path('super/users/<int:user_id>/', UserManageView.as_view(), name='user-manage'),
    
    # HR User Creation
    path('hr/staff/create/', HrUserCreateView.as_view(), name='hr-user-create'),    
    path('organization/', OrganizationView.as_view(), name='organization'),
]