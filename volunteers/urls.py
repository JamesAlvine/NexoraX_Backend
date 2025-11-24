
# volunteers/urls.py
from django.urls import path
from .views import VolunteerListView
urlpatterns = [path('volunteers/', VolunteerListView.as_view())]