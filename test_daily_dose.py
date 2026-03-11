import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.test import Client
from patients.models import Patient, DailyDose
from django.utils import timezone

def run_tests():
    Patient.objects.all().delete()
    
    # Create test data
    patient = Patient.objects.create(patient_id="PT-DOSE-01", name="Ethan Carter", gender="Male", age=32)
    
    today = timezone.now().date()
    
    # Create doses within last 7 days
    DailyDose.objects.create(patient=patient, date=today - datetime.timedelta(days=1), dose_amount=1.5)
    DailyDose.objects.create(patient=patient, date=today - datetime.timedelta(days=2), dose_amount=2.0)
    DailyDose.objects.create(patient=patient, date=today - datetime.timedelta(days=4), dose_amount=1.2)
    
    # Create an old dose (should not be returned)
    DailyDose.objects.create(patient=patient, date=today - datetime.timedelta(days=10), dose_amount=5.0)
    
    client = Client()
    
    print("Test 1: GET /api/patients/patients/{id}/recent_doses/")
    response = client.get(f'/api/patients/patients/{patient.id}/recent_doses/')
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data}\n")
        assert len(data) == 3, "Endpoint should only return doses from the last 7 days."
        print("Data length verified.")
        
        # Verify chronological order
        assert data[0]['dose_amount'] == 1.2
        assert data[1]['dose_amount'] == 2.0
        assert data[2]['dose_amount'] == 1.5
        print("Data ordering verified.")
        
    else:
        print(f"Response: {response.content}\n")
    assert response.status_code == 200
    
    print("All tests passed successfully!")

if __name__ == "__main__":
    run_tests()
