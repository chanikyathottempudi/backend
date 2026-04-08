from rest_framework import serializers
from .models import Patient, DailyDose, Alert

class AlertSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    room_number = serializers.CharField(source='patient.room_number', read_only=True)
    scan_type = serializers.SerializerMethodField()

    class Meta:
        model = Alert
        fields = ['id', 'patient', 'patient_name', 'room_number', 'scan_type', 'title', 'description', 
                  'alert_level', 'dose_value_mSv', 'is_active', 'created_at']

    def get_scan_type(self, obj):
        # Attempt to get the latest scan type from dicom registrations
        last_registration = getattr(obj.patient, 'scan_registrations', None)
        if last_registration and last_registration.exists():
            return last_registration.order_by('-registered_at').first().scan_type
        # Fallback if no specific registration found
        return "CT Scan"

class DailyDoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyDose
        fields = ['id', 'date', 'dose_amount']

class DicomScanSerializer(serializers.ModelSerializer):
    class Meta:
        from dicom.models import DicomScan
        model = DicomScan
        fields = ['id', 'file', 'uploaded_at', 'status']

class PatientSerializer(serializers.ModelSerializer):
    daily_doses = DailyDoseSerializer(many=True, read_only=True)
    alerts = AlertSerializer(many=True, read_only=True)
    dicom_scans = DicomScanSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'patient_id', 'name', 'gender', 'dob', 'age', 'blood_group', 'room_number', 'allergies', 'clinical_notes', 'daily_doses', 'alerts', 'dicom_scans']
