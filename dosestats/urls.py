from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScanDoseViewSet, OrganDoseViewSet, DoseAnomalyViewSet, DashboardViewSet, ScanParameterViewSet

router = DefaultRouter()
router.register(r'scans', ScanDoseViewSet)
router.register(r'organs', OrganDoseViewSet)
router.register(r'anomalies', DoseAnomalyViewSet)
router.register(r'dashboard', DashboardViewSet, basename='dashboard')
router.register(r'scan-parameters', ScanParameterViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
