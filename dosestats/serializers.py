from rest_framework import serializers
from .models import ScanDose, OrganDose, DoseAnomaly, ScanParameter

class OrganDoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganDose
        fields = ['id', 'organ_name', 'dose_value']

class ScanDoseSerializer(serializers.ModelSerializer):
    organ_doses = OrganDoseSerializer(many=True, read_only=True)

    class Meta:
        model = ScanDose
        fields = ['id', 'patient', 'scan_date', 'study_description', 'total_dlp', 'avg_risk', 'facility', 'organ_doses']

class DoseAnomalySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoseAnomaly
        fields = ['id', 'patient', 'anomaly_id', 'area', 'description', 'dlp_value', 'status_level', 'detected_at']

class ScanParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanParameter
        fields = ['id', 'patient', 'kvp', 'ma', 'pitch', 'scan_length', 'created_at']
