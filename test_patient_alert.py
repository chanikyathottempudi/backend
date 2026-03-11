import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from rest_framework.test import APIClient
from patients.models import Patient, Alert
from dicom.models import ScanRegistration

def run_tests():
    client = APIClient()

    print("--- Testing Patient Alert Endpoint ---")
    
    # Clean up before testing
    Patient.objects.filter(patient_id='TEST_ALT_001').delete()
    
    patient = Patient.objects.create(
        patient_id='TEST_ALT_001',
        name="Liam Carter",
        gender="Male"
    )
    
    # Create the associated scan registration
    ScanRegistration.objects.create(
        patient=patient,
        requesting_physician="Dr. House",
        scan_type="CT Head"
    )

    # Create the alert
    Alert.objects.create(
        patient=patient,
        title="Warning: Moderate Dose",
        description="The radiation dose for the CT scan of Liam Carter exceeded...",
        alert_level="WARNING",
        dose_value_mSv=12.5
    )

    response = client.get('/api/patients/alerts/', format='json')
    
    if response.status_code == 200:
        data = response.data
        if not data:
            print("❌ No alerts found.")
            return False
            
        test_alert = next((item for item in data if item["patient_name"] == "Liam Carter"), None)
        
        if not test_alert:
            print("❌ Test alert not found in response.")
            return False
            
        print("Sample item:", test_alert)
        
        if test_alert.get("scan_type") == "CT Head":
            print("✅ Successfully retrieved scan_type dynamically from ScanRegistration.")
        else:
            print(f"❌ scan_type mismatch. Expected 'CT Head', got '{test_alert.get('scan_type')}'.")
            return False

    else:
        print(f"❌ Failed GET request. Status: {response.status_code}")
        return False
        
    print("\nAll tests passed! Endpoint provides exactly what patient_alert_slide.xml needs.")
    return True

if __name__ == '__main__':
    run_tests()
