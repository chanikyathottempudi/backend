from django.urls import path
from .views import DicomScanViewSet, ScanRegistrationViewSet

urlpatterns = [
    path('scans/', DicomScanViewSet.as_view({'get': 'list', 'post': 'create'}), name='dicom-scans-list'),
    path('scans/<int:pk>/', DicomScanViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='dicom-scans-detail'),
    
    path('register-scan/', ScanRegistrationViewSet.as_view({'get': 'list', 'post': 'create'}), name='register-scan-list'),
    path('register-scan/<int:pk>/', ScanRegistrationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='register-scan-detail'),
]
