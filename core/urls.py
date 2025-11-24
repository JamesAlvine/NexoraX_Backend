# backend/core/urls.py
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include('hr.urls')),
    path('api/', include('volunteers.urls')),
]