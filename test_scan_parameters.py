import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.test import Client
from dosestats.models import ScanParameter

def run_tests():
    # Setup test data
    ScanParameter.objects.all().delete()
    
    client = Client()
    
    print("--- Testing Scan Parameters POST Endpoint ---")
    
    payload = {
        "kvp": 120.0,
        "ma": 250.5,
        "pitch": 1.25,
        "scan_length": 500.0
    }
    
    print(f"\nTesting POST /api/dosestats/scan-parameters/")
    response = client.post('/api/dosestats/scan-parameters/', data=payload, content_type='application/json')
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        print(f"Response Data: {data}")
        
        # Verify JSON response contains the saved data
        assert data['kvp'] == 120.0
        assert data['pitch'] == 1.25
        
        # Verify data is actually stored in the database
        db_count = ScanParameter.objects.count()
        assert db_count == 1
        
        saved_param = ScanParameter.objects.first()
        print(f"Database Record: {saved_param}")
        assert saved_param.kvp == 120.0
        assert saved_param.ma == 250.5
        
        print("-> POST Endpoint successfully created and stored the scan parameters.")
    else:
        print(f"Response: {response.content.decode('utf-8')}")
        assert False, "Scan Parameter POST API failed"
        
    print("\nAll Scan Parameters backend tests passed successfully!")

if __name__ == "__main__":
    run_tests()
