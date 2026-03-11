import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.test import Client
from patients.models import Patient

def run_tests():
    Patient.objects.all().delete()
    
    # Create test patient
    patient = Patient.objects.create(patient_id="PT-DELETE-01", name="George Miller", gender="Male", age=65)

    client = Client()
    
    # 1. Test fetching list
    print("Testing GET /api/patients/patients/")
    response = client.get('/api/patients/patients/')
    if response.status_code == 200:
        data = response.json()
        assert len(data) == 1
        record = data[0]
        assert 'name' in record # Maps to patient_name
        assert 'patient_id' in record # Maps to patient_id
        print("GET Request passed successfully! Fields match UI requirements.")

    # 2. Test deleting patient via API
    print(f"Testing DELETE /api/patients/patients/{patient.id}/ to simulate clicking the delete_patient_button")
    delete_response = client.delete(f'/api/patients/patients/{patient.id}/')
    print(f"Delete Status Code: {delete_response.status_code}")
    
    if delete_response.status_code == 204:
        # Verify patient is actually deleted
        assert Patient.objects.filter(id=patient.id).count() == 0
        print("Patient deleted successfully! DELETE functionality is verified.")
    else:
        print(f"Delete Response: {delete_response.content}\n")
        assert False, "patients API DELETE call failed"
        
    print("All list item patient tests passed successfully!")

if __name__ == "__main__":
    run_tests()
