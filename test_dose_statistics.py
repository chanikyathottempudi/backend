import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.test import Client
from patients.models import Patient
from dosestats.models import ScanDose
from django.utils import timezone

def run_tests():
    Patient.objects.all().delete()
    
    patient = Patient.objects.create(patient_id="PT-STATS-01", name="Bob Jones", gender="Male", age=50)
    
    # Create some scan doses
    ScanDose.objects.create(patient=patient, scan_date=timezone.now() - datetime.timedelta(days=2), study_description="CT Abdomen", total_dlp=300.0, avg_risk="Moderate")
    ScanDose.objects.create(patient=patient, scan_date=timezone.now() - datetime.timedelta(days=1), study_description="CT Pelvis", total_dlp=250.0, avg_risk="Low")
    ScanDose.objects.create(patient=patient, scan_date=timezone.now(), study_description="X-Ray Chest", total_dlp=10.0, avg_risk="Low")

    client = Client()
    
    print("Testing GET /api/dosestats/scans/by_patient/?patient_id=...")
    response = client.get(f'/api/dosestats/scans/by_patient/?patient_id={patient.id}')
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data}\n")
        assert len(data) == 3, f"Expected 3 records, got {len(data)}"
        
        # Verify the structure contains the required fields for statistics
        record = data[0]
        assert 'study_description' in record
        assert 'total_dlp' in record
        assert 'avg_risk' in record
        assert 'scan_date' in record
        
        print("All dosestats tests passed successfully!")
    else:
        print(f"Response: {response.content}\n")
        assert False, "dosestats API call failed"

if __name__ == "__main__":
    run_tests()
