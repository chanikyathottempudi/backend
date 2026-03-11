import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from rest_framework.test import APIClient
from patients.models import Patient
from dosestats.models import ScanDose
from django.utils import timezone
from datetime import timedelta

def run_tests():
    client = APIClient()

    print("--- Testing Patient Graph Endpoint ---")
    
    # Setup data
    Patient.objects.filter(patient_id='TEST_GRPH_001').delete()
    
    patient = Patient.objects.create(
        patient_id='TEST_GRPH_001',
        name="Ethan Carter",
        gender="Male"
    )
    
    now = timezone.now()
    ScanDose.objects.create(patient=patient, scan_date=now - timedelta(days=60), study_description="CT Head", total_dlp=40.5, avg_risk="Low")
    ScanDose.objects.create(patient=patient, scan_date=now - timedelta(days=30), study_description="CT Chest", total_dlp=60.0, avg_risk="Moderate")
    ScanDose.objects.create(patient=patient, scan_date=now, study_description="CT Abdomen", total_dlp=20.0, avg_risk="Low")

    # API Call
    response = client.get(f'/api/dosestats/scans/cumulative_trend/?patient_id={patient.id}', format='json')
    
    if response.status_code == 200:
        data = response.data
        print("✅ Successfully retrieved graph data (200 OK).")
        
        expected_total = 40.5 + 60.0 + 20.0
        if data.get("lifetime_total_dlp") == expected_total:
             print(f"✅ Lifetime total appropriately calculated: {expected_total}")
        else:
             print(f"❌ Lifetime total expectation failed. Expected {expected_total}, got {data.get('lifetime_total_dlp')}")
             return False
             
        if data.get("patient_name") == "Patient: Ethan Carter":
             print("✅ Patient name formatting is correct.")
        else:
             print(f"❌ Patient name formatting failed. Got '{data.get('patient_name')}'")
             return False
             
        trend_data = data.get("trend_data", [])
        if len(trend_data) == 3:
             print("✅ Trend data array has correct length (3 points for line chart).")
             print("Sample trend point:", trend_data[0])
        else:
             print("❌ Trend data array length incorrect.")
             return False

    else:
        print(f"❌ Failed GET request. Status: {response.status_code}")
        print(response.data)
        return False
        
    print("\nAll tests passed! Endpoint cumulative_trend provides exactly what patient_graph.xml needs.")
    return True

if __name__ == '__main__':
    run_tests()
