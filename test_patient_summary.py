import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from rest_framework.test import APIClient
from patients.models import Patient
from dosestats.models import ScanDose, OrganDose
from django.utils import timezone

def run_tests():
    client = APIClient()

    print("--- Testing Patient Summary (Organ Doses) Endpoint ---")
    
    # Setup data
    Patient.objects.filter(patient_id='TEST_SUM_001').delete()
    
    patient = Patient.objects.create(
        patient_id='TEST_SUM_001',
        name="Elena Roberts",
        gender="Female"
    )
    
    scan = ScanDose.objects.create(
        patient=patient,
        scan_date=timezone.now(),
        study_description="Full Body Scan",
        total_dlp=250.0,
        avg_risk="Moderate"
    )
    
    # Create the organ doses
    OrganDose.objects.create(scan=scan, organ_name="Head", dose_value=25.4)
    OrganDose.objects.create(scan=scan, organ_name="Chest", dose_value=110.2)
    OrganDose.objects.create(scan=scan, organ_name="Pelvis", dose_value=15.0)
    OrganDose.objects.create(scan=scan, organ_name="Abdomen", dose_value=40.1)
    OrganDose.objects.create(scan=scan, organ_name="Legs", dose_value=5.2)
    OrganDose.objects.create(scan=scan, organ_name="Arms", dose_value=6.8)

    # API Call
    response = client.get(f'/api/dosestats/scans/latest_organ_doses/?patient_id={patient.id}', format='json')
    
    if response.status_code == 200:
        data = response.data
        print("✅ Successfully retrieved latest organ doses (200 OK).")
        
        if data.get("patient_name") == "Patient: Elena Roberts":
             print("✅ Patient name mapping is correct.")
        else:
             print(f"❌ Patient name mapping failed. Got '{data.get('patient_name')}'")
             return False
             
        doses = data.get("doses", {})
        if not doses:
             print("❌ Doses dictionary missing from response.")
             return False
             
        print("Doses structured as:")
        for k, v in doses.items():
            print(f"  {k}: {v}")
            
        if doses.get("Chest") == 110.2 and doses.get("Arms") == 6.8:
             print("✅ Specific organ values correctly mapped into dictionary.")
        else:
             print("❌ Specific organ values mismatch.")
             return False

    else:
        print(f"❌ Failed GET request. Status: {response.status_code}")
        print(response.data)
        return False
        
    print("\nAll tests passed! Endpoint provides exactly what patient_summary.xml needs.")
    return True

if __name__ == '__main__':
    run_tests()
