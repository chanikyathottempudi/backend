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
            return Response({"error": "patient_id query parameter is required"}, status=400)
        
        # Get latest active dose readings
        recent_doses = self.queryset.filter(patient_id=patient_id).order_by('-timestamp')[:limit]
        
        # Sort chronologically for the chart
        recent_doses = reversed(recent_doses)
        
        serializer = self.get_serializer(recent_doses, many=True)
        return Response(serializer.data)
