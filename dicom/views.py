from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import DicomScan, ScanRegistration
from .serializers import DicomScanSerializer, ScanRegistrationSerializer

class DicomScanViewSet(viewsets.ModelViewSet):
    queryset = DicomScan.objects.all().order_by('-uploaded_at')
    serializer_class = DicomScanSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        patient_id = self.request.data.get('patient_id')
        if patient_id:
            try:
                from patients.models import Patient
                patient = Patient.objects.get(patient_id=patient_id)
                serializer.save(patient=patient, status='COMPLETED')
            except Patient.DoesNotExist:
                serializer.save(status='FAILED')
        else:
            serializer.save()

class ScanRegistrationViewSet(viewsets.ModelViewSet):
    queryset = ScanRegistration.objects.all().order_by('-registered_at')
    serializer_class = ScanRegistrationSerializer
