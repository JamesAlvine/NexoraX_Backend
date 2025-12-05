# backend/core/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include('hr.urls')),
    path('api/', include('volunteers.urls')),
    path('api/', include('crm.urls')),
    path('api/hr/', include('hr.urls')), 
    
]