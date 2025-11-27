from django.contrib import admin
from django.urls import path, include  # ✅ Added include import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include('hr.urls')),
    path('api/', include('volunteers.urls')),  # ✅ Added volunteers app URLs
    path('api/', include('crm.urls')),
    path('api/', include('crm.urls')),  # Added crm app URLs
    
]