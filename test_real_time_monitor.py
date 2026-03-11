import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.test import Client
from patients.models import Patient
from realtimemonitor.models import RealTimeDose

def run_tests():
    # Setup test data
    Patient.objects.all().delete()
    RealTimeDose.objects.all().delete()
    
    patient = Patient.objects.create(patient_id="PT-RTM-001", name="John Doe", gender="Male", age=35)
    
    # Create some real-time dose data
    RealTimeDose.objects.create(patient=patient, dose_rate=4.5, accumulated_dose=12.0)
    RealTimeDose.objects.create(patient=patient, dose_rate=4.8, accumulated_dose=16.8)
    
    client = Client()
    
    print("--- Testing Real-Time Monitor Endpoints ---")
    
    # 1. Test fetching patient list for the RecyclerView in real_time_monitor.xml
    print("\n1. Testing GET /api/patients/patients/ (for real_time_recycler_view)")
    response = client.get('/api/patients/patients/')
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Patients fetched: {len(data)}")
        assert len(data) >= 1
        record = data[0]
        assert 'name' in record
        assert 'patient_id' in record
        print("-> Patient list endpoint verified.")
    else:
        print(f"Response: {response.content}")
        assert False, "Patient list API failed"
        
    print(f"\n2. Testing GET /api/monitor/stream/?patient_id={patient.id} (for real-time updates)")
    response = client.get(f'/api/monitor/stream/?patient_id={patient.id}&limit=10')
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Stream data points fetched: {len(data)}")
        if len(data) != 2:
            print("ERROR: Stream data len is not 2. Data:", data)
            assert False, "Stream len mismatch"
        record = data[0]
        assert 'dose_rate' in record
        assert 'accumulated_dose' in record
        assert 'timestamp' in record
        print("-> Real-time stream endpoint verified.")
    else:
        print(f"Response: {response.content.decode('utf-8')}")
        assert False, "Real-time stream API failed"
        
    print("\nAll Real-Time Monitor backend tests passed successfully!")

if __name__ == "__main__":
    run_tests()
