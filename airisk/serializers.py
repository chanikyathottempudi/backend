from rest_framework import serializers
from .models import PatientRiskAssessment

class PatientRiskAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientRiskAssessment
        fields = '__all__'
