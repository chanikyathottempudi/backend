import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.test import Client
from patients.models import Patient, Alert
from dosestats.models import ScanDose, DoseAnomaly
from django.utils import timezone

def run_tests():
    # Clear existing data to avoid conflicts for this quick test
    Patient.objects.all().delete()
    
    # Create test data
    patient = Patient.objects.create(patient_id="PT-DASH-01", name="John Doe", gender="Male", age=40)
    today = timezone.now().date()
    
    # Create 3 scans today
    ScanDose.objects.create(patient=patient, scan_date=timezone.now(), study_description="CT Head", total_dlp=100.0, avg_risk="Low")
    ScanDose.objects.create(patient=patient, scan_date=timezone.now(), study_description="CT Chest", total_dlp=150.0, avg_risk="Moderate")
    ScanDose.objects.create(patient=patient, scan_date=timezone.now(), study_description="X-Ray", total_dlp=5.0, avg_risk="Low")

    # Create 2 active alerts
    Alert.objects.create(patient=patient, title="High Dose", description="Dose over limit", alert_level="WARNING", is_active=True)
    Alert.objects.create(patient=patient, title="Critical Issue", description="Immediate action", alert_level="CRITICAL", is_active=True)
    
    # Create 1 inactive alert (should not be counted)
    Alert.objects.create(patient=patient, title="Old Alert", description="Resolved", alert_level="INFO", is_active=False)

    # Create 1 anomaly for today
    DoseAnomaly.objects.create(patient=patient, anomaly_id="ANOM-001", area="Head", description="High Dose", dlp_value=25.0, status_level="HIGH")

    client = Client()
    
    print("Testing GET /api/dosestats/dashboard/")
    response = client.get('/api/dosestats/dashboard/')
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data}\n")
        
        # We expect:
        # total_scans_today = 3
        # active_alerts_count = 2
        # safety_compliance_percentage = 100 - (1 anomaly * 5) = 95
        assert data['total_scans_today'] == 3, f"Expected 3 scans, got {data['total_scans_today']}"
        assert data['active_alerts_count'] == 2, f"Expected 2 alerts, got {data['active_alerts_count']}"
        assert data['safety_compliance_percentage'] == 95, f"Expected 95% compliance, got {data['safety_compliance_percentage']}"
        print("All dashboard tests passed successfully!")
    else:
        print(f"Response: {response.content}\n")
        assert False, "Dashboard API call failed"

if __name__ == "__main__":
    run_tests()
