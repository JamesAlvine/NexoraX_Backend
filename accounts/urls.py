from django.urls import path
from .views import csrf, LoginView, MeView, UserListView, OrganizationView

urlpatterns = [
    path('auth/csrf/', csrf, name='csrf'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/me/', MeView.as_view(), name='me'),
    path('super/users/', UserListView.as_view(), name='user_list'),
    path('super/organization/', OrganizationView.as_view(), name='organization'),
]