# hr/urls.py
from django.urls import path
from .views import StaffListView
urlpatterns = [path('staff/', StaffListView.as_view())]
