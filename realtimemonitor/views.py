from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import RealTimeDose
from .serializers import RealTimeDoseSerializer

class RealTimeDoseViewSet(viewsets.ModelViewSet):
    queryset = RealTimeDose.objects.all()
    serializer_class = RealTimeDoseSerializer

    @action(detail=False, methods=['get'])
    def stream(self, request):
        """
        Endpoint to fetch the most recent data points for the real-time line chart.
        Pass ?patient_id=X&limit=20 to get the last 20 readings for a patient.
        """
        patient_id = request.query_params.get('patient_id')
        try:
            limit = int(request.query_params.get('limit', 20))
        except ValueError:
            limit = 20

        if not patient_id:
            return Response({"success": False, "error": "patient_id query parameter is required"}, status=400)
        
        # Get latest active dose readings
        recent_doses = self.queryset.filter(patient__patient_id=patient_id).order_by('-timestamp')[:limit]
        
        # Threshold Check and Alert Triggering
        threshold = 1.5 # Example threshold for real-time dose rate (mSv/hr)
        for dose in recent_doses:
            if dose.is_active and dose.dose_rate > threshold:
                from patients.models import Alert
                Alert.objects.get_or_create(
                    patient=dose.patient,
                    title="CRITICAL: Real-time Dose Exceeded",
                    defaults={
                        "description": f"Dose rate {dose.dose_rate} mSv/hr detected at {dose.timestamp}. Safety threshold is {threshold}.",
                        "alert_level": "CRITICAL",
                        "dose_value_mSv": dose.dose_rate
                    }
                )
                # Simulated push notification
                from .notifications import send_push_notification
                send_push_notification(
                    dose.patient.user if hasattr(dose.patient, 'user') else None, 
                    "Critical Dose Alert", 
                    f"A critical dose rate of {dose.dose_rate} mSv/hr was detected for patient {dose.patient.name}."
                )

        # Sort chronologically for the chart
        recent_doses = reversed(recent_doses)
        
        serializer = self.get_serializer(recent_doses, many=True)
        return Response({"success": True, "data": serializer.data})
