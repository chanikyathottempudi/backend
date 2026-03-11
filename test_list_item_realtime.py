import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.test import Client
from patients.models import Patient

def run_tests():
    Patient.objects.all().delete()
    
    # Create test patient
    patient = Patient.objects.create(patient_id="PT-REALTIME-01", name="Isabella Swan", gender="Female", age=18)

    client = Client()
    
    print("Testing GET /api/patients/patients/")
    response = client.get('/api/patients/patients/')
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data}\n")
        assert len(data) == 1
        
        # Verify fields map to list_item_real_time_monitor.xml
        record = data[0]
        assert 'name' in record # Maps to patient_name_real_time
        assert 'patient_id' in record # Maps to patient_id_real_time
        
        print("All list item real time monitor tests passed successfully!")
    else:
        print(f"Response: {response.content}\n")
        assert False, "patients API call failed"

if __name__ == "__main__":
    run_tests()
