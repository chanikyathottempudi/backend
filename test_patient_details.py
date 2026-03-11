import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.test import Client
from patients.models import Patient
from dicom.models import DicomScan
from django.utils import timezone

def run_tests():
    Patient.objects.all().delete()
    
    # Create test patient
    patient = Patient.objects.create(
        patient_id="123456789", 
        name="Ethan Carter", 
        gender="Male", 
        age=32,
        allergies="None",
        clinical_notes="Patient is doing well."
    )
    
    # Create mock dicom scans
    DicomScan.objects.create(patient=patient, uploaded_at=timezone.now(), status="Processed")
    DicomScan.objects.create(patient=patient, uploaded_at=timezone.now(), status="Pending")
    
    client = Client()
    
    print(f"Testing GET /api/patients/patients/{patient.id}/")
    response = client.get(f'/api/patients/patients/{patient.id}/')
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data}\n")
        
        # Verify required fields for details_patient.xml
        assert data['name'] == "Ethan Carter"
        assert data['gender'] == "Male"
        assert data['age'] == 32
        assert data['patient_id'] == "123456789"
        assert data['allergies'] == "None"
        assert 'dicom_scans' in data
        assert len(data['dicom_scans']) == 2
        
        print("All patient details tests passed successfully!")
    else:
        print(f"Response: {response.content}\n")
        assert False, "Patient details API call failed"

if __name__ == "__main__":
    run_tests()
