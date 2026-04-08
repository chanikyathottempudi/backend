from django.urls import path
from .views import PatientViewSet, DailyDoseViewSet, AlertViewSet

urlpatterns = [
    # Patient ViewSet explicit paths
    path('patients/', PatientViewSet.as_view({'get': 'list', 'post': 'create'}), name='patient-list'),
    path('patients/<int:pk>/', PatientViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='patient-detail'),
    path('patients/<int:pk>/recent_doses/', PatientViewSet.as_view({'get': 'recent_doses'}), name='patient-recent-doses'),
    path('patients/<int:pk>/active_critical_alert/', PatientViewSet.as_view({'get': 'active_critical_alert'}), name='patient-active-critical-alert'),
    path('patients/<int:pk>/emergency_stop/', PatientViewSet.as_view({'post': 'emergency_stop'}), name='patient-emergency-stop'),
    path('patients/<int:pk>/call_supervisor/', PatientViewSet.as_view({'post': 'call_supervisor'}), name='patient-call-supervisor'),

    # DailyDose ViewSet explicit paths
    path('daily-doses/', DailyDoseViewSet.as_view({'get': 'list', 'post': 'create'}), name='dailydose-list'),
    path('daily-doses/<int:pk>/', DailyDoseViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='dailydose-detail'),

    # Alert ViewSet explicit paths
    path('alerts/', AlertViewSet.as_view({'get': 'list', 'post': 'create'}), name='alert-list'),
    path('alerts/<int:pk>/', AlertViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='alert-detail'),
    path('alerts/active_count/', AlertViewSet.as_view({'get': 'active_count'}), name='alert-active-count'),
]
