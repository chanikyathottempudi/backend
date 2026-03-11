import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from rest_framework.test import APIClient
from patients.models import Patient
from dicom.models import ScanRegistration

def run_tests():
    client = APIClient()

    print("--- Testing New Scans GET Endpoint ---")
    
    # Setup Data
    Patient.objects.filter(patient_id='TEST_LST_001').delete()
    
    patient = Patient.objects.create(
        patient_id='TEST_LST_001',
        name="Test Patient 001",
        gender="Male",
        clinical_notes="Patient presents with acute head trauma."
    )
    
    ScanRegistration.objects.create(
        patient=patient,
        requesting_physician="Dr. Gregory House",
        scan_type="CT Head"
    )

    response = client.get('/api/dicom/register-scan/', format='json')
    
    if response.status_code == 200:
        print("✅ Successfully retrieved scan registrations (200 OK).")
        data = response.data
        
        # Check if we got results
        if not data:
            print("❌ No data returned.")
            return False
            
        print("Sample item:", data[0])
            
        # Verify the structure has our new fields
        first_item = data[0]
        missing_fields = []
        expected_fields = ['patient_name_display', 'clinical_indication', 'requesting_physician', 'scan_type']
        
        for field in expected_fields:
            if field not in first_item:
                missing_fields.append(field)
                
        if missing_fields:
            print(f"❌ Missing expected fields in response: {missing_fields}")
            return False
        
        if first_item['patient_name_display'] == "Test Patient 001" and first_item['clinical_indication'] == "Patient presents with acute head trauma.":
             print("✅ Display fields populated correctly from Patient relation.")
        else:
             print("❌ Display fields did not match expected actual values.")
             return False
             
    else:
        print(f"❌ Failed GET request. Status: {response.status_code}")
        return False
        
    print("\nAll tests passed! Endpoint provides exactly what new_scans.xml needs.")
    return True

if __name__ == '__main__':
    run_tests()
