import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from rest_framework.test import APIClient
from patients.models import Patient
from dicom.models import ScanRegistration

def run_tests():
    client = APIClient()

    print("--- Testing New Scan Registration ---")
    
    # Clean up before testing
    Patient.objects.filter(patient_id='TEST_PT_999').delete()
    
    data = {
        "patient_name": "Test Patient",
        "patient_id": "TEST_PT_999",
        "requesting_physician": "Dr. Smith",
        "scan_type": "CT"
    }

    response = client.post('/api/dicom/register-scan/', data, format='json')
    
    if response.status_code == 201:
        print("✅ Scan registered successfully (201 Created).")
    else:
        print(f"❌ Failed to register scan. Status: {response.status_code}")
        print(response.data)
        return False
        
    print("\n--- Verifying Database Records ---")
    patient_exists = Patient.objects.filter(patient_id='TEST_PT_999').exists()
    registration_exists = ScanRegistration.objects.filter(requesting_physician='Dr. Smith', patient__patient_id='TEST_PT_999').exists()
    
    if patient_exists:
        print("✅ Patient record was created or found successfully.")
    else:
        print("❌ Patient record was NOT created.")
        return False

    if registration_exists:
        print("✅ ScanRegistration record was created successfully.")
    else:
        print("❌ ScanRegistration record was NOT created.")
        return False
        
    print("\nAll tests passed! Endpoint is ready for new_scans_register.xml.")
    return True

if __name__ == '__main__':
    run_tests()
