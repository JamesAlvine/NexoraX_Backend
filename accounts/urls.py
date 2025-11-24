# backend/accounts/urls.py
from django.urls import path
from .views import csrf, LoginView, UserCreateView

urlpatterns = [
    path('auth/csrf/', csrf),
    path('auth/login/', LoginView.as_view()),
    path('users/create/', UserCreateView.as_view()),
]