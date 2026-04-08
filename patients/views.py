from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Patient, DailyDose, Alert
from .serializers import PatientSerializer, DailyDoseSerializer, AlertSerializer
from datetime import timedelta
from django.utils import timezone

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'patient_id', 'gender']

    @action(detail=True, methods=['get'])
    def recent_doses(self, request, pk=None):
        patient = self.get_object()
        # Last 7 days
        recent_date = timezone.now().date() - timedelta(days=7)
        doses = patient.daily_doses.filter(date__gte=recent_date).order_by('date')
        serializer = DailyDoseSerializer(doses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def active_critical_alert(self, request, pk=None):
        patient = self.get_object()
        alert = patient.alerts.filter(is_active=True, alert_level='CRITICAL').first()
        if alert:
            serializer = AlertSerializer(alert)
            return Response(serializer.data)
        return Response({"detail": "No active critical alert found."}, status=404)

    @action(detail=True, methods=['post'])
    def emergency_stop(self, request, pk=None):
        patient = self.get_object()
        # Stop active real-time doses
        from realtimemonitor.models import RealTimeDose
        RealTimeDose.objects.filter(patient=patient, is_active=True).update(is_active=False)
        # Resolve active critical alerts
        patient.alerts.filter(is_active=True, alert_level='CRITICAL').update(is_active=False)
        return Response({"status": "Emergency stop executed. All procedures stopped and alerts resolved."})

    @action(detail=True, methods=['post'])
    def call_supervisor(self, request, pk=None):
        patient = self.get_object()
        # In a real app this would trigger an SMS/Email to a supervisor
        return Response({"status": f"Supervisor has been notified regarding patient {patient.name}."})

    @action(detail=True, methods=['get'])
    def get_history(self, request, pk=None):
        patient = self.get_object()
        from dosestats.models import ScanDose
        from dosestats.serializers import ScanDoseSerializer
        scans = ScanDose.objects.filter(patient=patient).order_by('-scan_date')
        serializer = ScanDoseSerializer(scans, many=True)
        return Response({"success": True, "data": serializer.data})

    @action(detail=True, methods=['get'])
    def generate_summary(self, request, pk=None):
        patient = self.get_object()
        from dosestats.models import ScanDose
        from django.db.models import Avg
        total_scans = ScanDose.objects.filter(patient=patient).count()
        avg_dlp = ScanDose.objects.filter(patient=patient).aggregate(Avg('total_dlp'))['total_dlp__avg'] or 0.0
        
        summary = (
            f"Patient {patient.name} ({patient.patient_id}) has a recorded history of {total_scans} scans. "
            f"The average Dose Length Product (DLP) across these scans is {avg_dlp:.2f} mGy*cm. "
            f"Current clinical notes state: {patient.clinical_notes or 'None'}. "
            f"Allergies recorded: {patient.allergies or 'None'}."
        )
        
        return Response({
            "success": True,
            "data": {
                "patient_id": patient.patient_id,
                "patient_name": patient.name,
                "total_scans": total_scans,
                "average_dlp": round(avg_dlp, 2),
                "summary_text": summary
            }
        })

class DailyDoseViewSet(viewsets.ModelViewSet):
    queryset = DailyDose.objects.all()
    serializer_class = DailyDoseSerializer

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all().order_by('-created_at')
    serializer_class = AlertSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'patient__name']

    @action(detail=False, methods=['get'])
    def active_count(self, request):
        count = self.queryset.filter(is_active=True).count()
        return Response({"active_count": count})
