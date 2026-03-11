import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.test import Client
from patients.models import Patient, Alert
from realtimemonitor.models import RealTimeDose

def run_tests():
    Patient.objects.all().delete()
    
    # Create test data
    patient = Patient.objects.create(patient_id="PT12345", name="Liam Carter", gender="Male", age=45)
    
    alert = Alert.objects.create(
        patient=patient,
        title="Dose Limit Exceeded",
        description="The radiation dose has exceeded the critical threshold. Immediate action is required.",
        alert_level="CRITICAL",
        dose_value_mSv=1500.0,
        is_active=True
    )
    
    RealTimeDose.objects.create(
        patient=patient,
        dose_rate=10.5,
        accumulated_dose=1500.0,
        is_active=True
    )
    
    client = Client()
    
    # Test 1: Get active critical alert
    print("Test 1: GET /api/patients/patients/{id}/active_critical_alert/")
    response = client.get(f'/api/patients/patients/{patient.id}/active_critical_alert/')
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}\n")
    else:
        print(f"Response: {response.content}\n")
    assert response.status_code == 200
    
    # Test 2: Call Supervisor
    print("Test 2: POST /api/patients/patients/{id}/call_supervisor/")
    response = client.post(f'/api/patients/patients/{patient.id}/call_supervisor/')
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}\n")
    else:
        print(f"Response: {response.content}\n")
    assert response.status_code == 200
    
    # Test 3: Emergency Stop
    print("Test 3: POST /api/patients/patients/{id}/emergency_stop/")
    response = client.post(f'/api/patients/patients/{patient.id}/emergency_stop/')
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}\n")
    else:
        print(f"Response: {response.content}\n")
    assert response.status_code == 200
    
    # Verify database state after emergency stop
    alert.refresh_from_db()
    assert alert.is_active == False
    
    rtd = RealTimeDose.objects.filter(patient=patient).first()
    assert rtd.is_active == False
    
    print("All tests passed successfully!")

if __name__ == "__main__":
    run_tests()
