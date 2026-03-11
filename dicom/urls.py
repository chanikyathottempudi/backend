from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DicomScanViewSet, ScanRegistrationViewSet

router = DefaultRouter()
router.register(r'scans', DicomScanViewSet)
router.register(r'register-scan', ScanRegistrationViewSet, basename='register-scan')

urlpatterns = [
    path('', include(router.urls)),
]
