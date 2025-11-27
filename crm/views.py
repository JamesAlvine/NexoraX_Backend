# backend/crm/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Donor, Beneficiary

User = get_user_model()

class DonorListView(APIView):
    def get(self, request):
        if not request.user.is_superuser:
            return Response({'error': 'Access denied'}, status=403)
        donors = Donor.objects.values('id', 'name', 'email', 'total_given')
        return Response(list(donors))

    def post(self, request):
        if not request.user.is_superuser:
            return Response({'error': 'Access denied'}, status=403)
        # Simplified donor creation
        donor = Donor.objects.create(
            organization_id=1,  # Assumes you have an Organization
            name=request.data.get('name', ''),
            email=request.data.get('email', ''),
            phone=request.data.get('phone', '')
        )
        return Response({'id': donor.id, 'name': donor.name}, status=201)

class BeneficiaryListView(APIView):
    def get(self, request):
        if not request.user.is_superuser:
            return Response({'error': 'Access denied'}, status=403)
        beneficiaries = Beneficiary.objects.values('id', 'unique_id', 'name')
        return Response(list(beneficiaries))

    def post(self, request):
        if not request.user.is_superuser:
            return Response({'error': 'Access denied'}, status=403)
        beneficiary = Beneficiary.objects.create(
            organization_id=1,
            unique_id=request.data.get('unique_id', ''),
            name=request.data.get('name', ''),
            needs=request.data.get('needs', '').split(', ')
        )
        return Response({'id': beneficiary.id, 'name': beneficiary.name}, status=201)