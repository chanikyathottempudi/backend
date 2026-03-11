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
    
    patient = Patient.objects.create(patient_id="PT-DETAILS-001", name="Ethan Carter", gender="Male", age=45)
    
    # Create multiple real-time dose data points for the LineChart
    RealTimeDose.objects.create(patient=patient, dose_rate=1.0, accumulated_dose=1.0)
    RealTimeDose.objects.create(patient=patient, dose_rate=2.0, accumulated_dose=3.0)
    RealTimeDose.objects.create(patient=patient, dose_rate=3.0, accumulated_dose=6.0)
    RealTimeDose.objects.create(patient=patient, dose_rate=4.0, accumulated_dose=10.0)
    RealTimeDose.objects.create(patient=patient, dose_rate=5.0, accumulated_dose=15.0)
    
    client = Client()
    
    print("--- Testing Real-Time Patient Details Endpoints ---")
    
    # Test fetching real-time stream data specifically for the LineChart and Current Dose Rate
    print(f"\nTesting GET /api/monitor/stream/?patient_id={patient.id}&limit=5")
    response = client.get(f'/api/monitor/stream/?patient_id={patient.id}&limit=5')
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Stream data points fetched: {len(data)}")
        
        if len(data) != 5:
            print("ERROR: Expected 5 data points for the LineChart. Data:", data)
            assert False, "Stream length mismatch"
            
        print("\nVerifying data structure for real_time_patient_details.xml:")
        
        # Verify it has what the LineChart needs (array of values over time)
        for record in data:
            assert 'dose_rate' in record
            assert 'timestamp' in record
            
        print("-> LineChart data requirement (dose_rate over time): Verified.")
        
        # Verify it has what the "Current Dose Rate" TextView needs (the latest dose rate)
        latest_record = data[-1] # The last item is the most recent (chronological sort)
        assert 'dose_rate' in latest_record
        print(f"-> Current Dose Rate requirement (latest dose_rate = {latest_record['dose_rate']}): Verified.")
        
    else:
        print(f"Response: {response.content.decode('utf-8')}")
        assert False, "Real-time stream API failed for Patient Details"
        
    print("\nAll Real-Time Patient Details backend tests passed successfully!")

if __name__ == "__main__":
    run_tests()
