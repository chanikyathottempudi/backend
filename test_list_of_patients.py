import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.test import Client
from patients.models import Patient

def run_tests():
    Patient.objects.all().delete()
    
    # Create test patients to populate the ListView
    Patient.objects.create(patient_id="PT-LIST-01", name="Alpha Patient", gender="Male", age=41)
    Patient.objects.create(patient_id="PT-LIST-02", name="Beta Patient", gender="Female", age=33)

    client = Client()
    
    print("Testing GET /api/patients/patients/ for list of patients view")
    response = client.get('/api/patients/patients/')
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data}\n")
        assert len(data) == 2
        print("GET Request passed successfully! The endpoint provides an array of patients suitable for populating a ListView.")
    else:
        print(f"Response: {response.content}\n")
        assert False, "patients API call failed"

if __name__ == "__main__":
    run_tests()
