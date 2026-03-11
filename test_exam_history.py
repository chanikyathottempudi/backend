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
    
    patient = Patient.objects.create(patient_id="PT-EXAM-01", name="Sarah Connor", gender="Female", age=35)
    
    # Create an exam with facility
    ScanDose.objects.create(
        patient=patient, 
        scan_date=timezone.now(), 
        study_description="CT Head", 
        total_dlp=1200.0, 
        avg_risk="Moderate",
        facility="Facility A"
    )

    client = Client()
    
    print("Testing GET /api/dosestats/scans/by_patient/?patient_id=...")
    response = client.get(f'/api/dosestats/scans/by_patient/?patient_id={patient.id}')
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data}\n")
        assert len(data) == 1
        
        # Verify fields required by exam_history_item.xml
        record = data[0]
        assert 'study_description' in record # Exam name (CT Head)
        assert 'scan_date' in record # Date (2023-08-15)
        assert 'facility' in record # Facility (Facility A)
        assert 'total_dlp' in record # DLP (1200 mGy*cm)
        
        print("All exam history item tests passed successfully!")
    else:
        print(f"Response: {response.content}\n")
        assert False, "dosestats API call failed"

if __name__ == "__main__":
    run_tests()
