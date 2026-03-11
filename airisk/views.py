from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PatientRiskAssessment
from .serializers import PatientRiskAssessmentSerializer

class PatientRiskAssessmentViewSet(viewsets.ModelViewSet):
    queryset = PatientRiskAssessment.objects.all()
    serializer_class = PatientRiskAssessmentSerializer

    @action(detail=False, methods=['get'])
    def by_patient(self, request):
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response({"error": "patient_id parameter is required"}, status=400)
            
        try:
            assessment = PatientRiskAssessment.objects.get(patient_id=patient_id)
            serializer = self.get_serializer(assessment)
            return Response(serializer.data)
        except PatientRiskAssessment.DoesNotExist:
            return Response({"error": "No risk assessment found for this patient"}, status=404)
