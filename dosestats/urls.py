from django.urls import path
from .views import ScanDoseViewSet, OrganDoseViewSet, DoseAnomalyViewSet, DashboardViewSet, ScanParameterViewSet

urlpatterns = [
    # ScanDose ViewSet explicit paths
    path('scans/', ScanDoseViewSet.as_view({'get': 'list', 'post': 'create'}), name='scandose-list'),
    path('scans/<int:pk>/', ScanDoseViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='scandose-detail'),
    path('scans/by_patient/', ScanDoseViewSet.as_view({'get': 'by_patient'}), name='scandose-by-patient'),
    path('scans/average_dlp/', ScanDoseViewSet.as_view({'get': 'average_dlp'}), name='scandose-average-dlp'),
    path('scans/monthly_summary/', ScanDoseViewSet.as_view({'get': 'monthly_summary'}), name='scandose-monthly-summary'),
    path('scans/monthly_heatmap/', ScanDoseViewSet.as_view({'get': 'monthly_heatmap'}), name='scandose-monthly-heatmap'),
    path('scans/cumulative_trend/', ScanDoseViewSet.as_view({'get': 'cumulative_trend'}), name='scandose-cumulative-trend'),
    path('scans/latest_organ_doses/', ScanDoseViewSet.as_view({'get': 'latest_organ_doses'}), name='scandose-latest-organ-doses'),
    path('scans/predict_dose/', ScanDoseViewSet.as_view({'post': 'predict_dose'}), name='scandose-predict-dose'),
    path('scans/daily_trend/', ScanDoseViewSet.as_view({'get': 'daily_trend'}), name='scandose-daily-trend'),
    path('scans/monthly_trend/', ScanDoseViewSet.as_view({'get': 'monthly_trend'}), name='scandose-monthly-trend'),
    path('scans/dose_statistics/', ScanDoseViewSet.as_view({'get': 'dose_statistics'}), name='scandose-dose-statistics'),
    path('scans/detect_anomalies/', ScanDoseViewSet.as_view({'post': 'detect_anomalies'}), name='scandose-detect-anomalies'),

    # OrganDose ViewSet explicit paths
    path('organs/', OrganDoseViewSet.as_view({'get': 'list', 'post': 'create'}), name='organdose-list'),
    path('organs/<int:pk>/', OrganDoseViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='organdose-detail'),

    # DoseAnomaly ViewSet explicit paths
    path('anomalies/', DoseAnomalyViewSet.as_view({'get': 'list', 'post': 'create'}), name='doseanomaly-list'),
    path('anomalies/<int:pk>/', DoseAnomalyViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='doseanomaly-detail'),

    # Dashboard ViewSet explicit paths
    path('dashboard/', DashboardViewSet.as_view({'get': 'list'}), name='dashboard'),

    # ScanParameter ViewSet explicit paths
    path('scan-parameters/', ScanParameterViewSet.as_view({'get': 'list', 'post': 'create'}), name='scanparameter-list'),
    path('scan-parameters/<int:pk>/', ScanParameterViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='scanparameter-detail'),
]
