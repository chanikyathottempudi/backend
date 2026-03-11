from rest_framework import serializers
from .models import DicomScan, ScanRegistration
from patients.models import Patient

class DicomScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DicomScan
        fields = ['id', 'patient', 'file', 'uploaded_at', 'status']

class ScanRegistrationSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(write_only=True)
    patient_id = serializers.CharField(write_only=True)
    
    # Read-only fields to satisfy new_scans.xml layout
    patient_name_display = serializers.CharField(source='patient.name', read_only=True)
    clinical_indication = serializers.CharField(source='patient.clinical_notes', read_only=True)

    class Meta:
        model = ScanRegistration
        fields = ['id', 'patient', 'patient_name', 'patient_id', 'patient_name_display', 'clinical_indication', 'requesting_physician', 'scan_type', 'registered_at', 'status']
        read_only_fields = ['patient', 'patient_name_display', 'clinical_indication', 'registered_at', 'status']

    def create(self, validated_data):
        patient_name = validated_data.pop('patient_name')
        patient_id_val = validated_data.pop('patient_id')
        
        patient, _ = Patient.objects.get_or_create(
            patient_id=patient_id_val,
            defaults={'name': patient_name, 'gender': 'Unknown'}
        )
        
        scan_registration = ScanRegistration.objects.create(patient=patient, **validated_data)
        return scan_registration
