from django.urls import path
from .views import PatientRiskAssessmentViewSet

urlpatterns = [
    path('assessments/', PatientRiskAssessmentViewSet.as_view({'get': 'list', 'post': 'create'}), name='airisk-assessments-list'),
    path('assessments/<int:pk>/', PatientRiskAssessmentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='airisk-assessments-detail'),
    path('assessments/by_patient/', PatientRiskAssessmentViewSet.as_view({'get': 'by_patient'}), name='airisk-assessments-by-patient'),
    path('assessments/calculate_risk/', PatientRiskAssessmentViewSet.as_view({'post': 'calculate_risk'}), name='airisk-assessments-calculate-risk'),
]
