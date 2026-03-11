import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.test import Client
from patients.models import Patient
from dosestats.models import ScanDose, DoseAnomaly
from django.utils import timezone

def run_tests():
    Patient.objects.all().delete()
    
    patient = Patient.objects.create(patient_id="PT-ANOM-01", name="Alice Smith", gender="Female", age=28)
    
    # Create scan doses for avg
    ScanDose.objects.create(patient=patient, scan_date=timezone.now(), study_description="CT Head", total_dlp=400.0, avg_risk="Moderate")
    ScanDose.objects.create(patient=patient, scan_date=timezone.now(), study_description="CT Head", total_dlp=440.0, avg_risk="Moderate")
    
    # Create anomaly
    DoseAnomaly.objects.create(patient=patient, anomaly_id="ANOM-002", area="Head", description="Unusually high dose for standard CT.", dlp_value=440.0, status_level="HIGH")

    client = Client()
    
    print("Testing GET /api/dosestats/anomalies/?patient_id=...")
    response = client.get(f'/api/dosestats/anomalies/?patient_id={patient.id}')
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Anomalies Response: {data}\n")
        assert len(data) == 1
    else:
        print(f"Error Response: {response.content}\n")
        assert False
        
    print("Testing GET /api/dosestats/scans/average_dlp/?patient_id=...")
    response = client.get(f'/api/dosestats/scans/average_dlp/?patient_id={patient.id}')
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Average DLP Response: {data}\n")
        assert data['average_dlp'] == 420.0
    else:
        print(f"Error Response: {response.content}\n")
        assert False

    print("All tests passed successfully!")

if __name__ == "__main__":
    run_tests()
