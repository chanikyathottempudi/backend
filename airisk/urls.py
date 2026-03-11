from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientRiskAssessmentViewSet

router = DefaultRouter()
router.register(r'assessments', PatientRiskAssessmentViewSet, basename='airisk-assessments')

urlpatterns = [
    path('', include(router.urls)),
]
