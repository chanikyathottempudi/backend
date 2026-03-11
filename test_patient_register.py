import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from rest_framework.test import APIClient
from patients.models import Patient
import datetime

def run_tests():
    client = APIClient()

    print("--- Testing Patient Registration Endpoint ---")
    
    # Clean up before testing
    Patient.objects.filter(patient_id='TEST_REG_123').delete()
    
    # Data as collected by patient_register.xml
    data = {
        "name": "Jane Doe",
        "dob": "1990-05-15",
        "gender": "Female",
        "patient_id": "TEST_REG_123",
        "allergies": "Penicillin"
    }

    # POST to patients endpoint
    response = client.post('/api/patients/patients/', data, format='json')
    
    if response.status_code == 201:
        print("✅ Patient created successfully (201 Created).")
    else:
        print(f"❌ Failed to create patient. Status: {response.status_code}")
        print(response.data)
        return False
        
    print("\n--- Verifying Database Record ---")
    patient_exists = Patient.objects.filter(patient_id='TEST_REG_123').exists()
    
    if patient_exists:
        patient = Patient.objects.get(patient_id='TEST_REG_123')
        print("✅ Patient record was created successfully.")
        
        if patient.dob == datetime.date(1990, 5, 15):
             print(f"✅ Patient dob saved successfully: {patient.dob}")
        else:
             print(f"❌ Patient dob mismatch. Expected '1990-05-15', got '{patient.dob}'")
             return False
             
        if patient.allergies == "Penicillin":
            print(f"✅ Patient allergies saved successfully: {patient.allergies}")
        else:
            print(f"❌ Patient allergies mismatch.")
            return False
            
    else:
        print("❌ Patient record was NOT created.")
        return False

    print("\nAll tests passed! Endpoint seamlessly integrates with patient_register.xml.")
    return True

if __name__ == '__main__':
    run_tests()
