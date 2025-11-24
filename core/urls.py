from django.contrib import admin
from django.urls import path, include  # ✅ include is used here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include('hr.urls')),
    path('api/', include('volunteers.urls')),
]