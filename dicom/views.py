from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import DicomScan, ScanRegistration
from .serializers import DicomScanSerializer, ScanRegistrationSerializer

class DicomScanViewSet(viewsets.ModelViewSet):
    queryset = DicomScan.objects.all().order_by('-uploaded_at')
    serializer_class = DicomScanSerializer
    parser_classes = (MultiPartParser, FormParser) # Ensures that the view accepts file data

class ScanRegistrationViewSet(viewsets.ModelViewSet):
    queryset = ScanRegistration.objects.all().order_by('-registered_at')
    serializer_class = ScanRegistrationSerializer
