# backend/crm/urls.py
from django.urls import path
from .views import DonorListView, BeneficiaryListView

urlpatterns = [
    path('donors/', DonorListView.as_view()),
    path('beneficiaries/', BeneficiaryListView.as_view()),
]