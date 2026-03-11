import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.test import Client
from admincenter.models import SystemLog
from django.utils import timezone

def run_tests():
    SystemLog.objects.all().delete()
    
    # Create test log entries
    SystemLog.objects.create(
        level="WARNING",
        message="User authentication failed 3 times.",
        source="Auth"
    )
    SystemLog.objects.create(
        level="INFO",
        message="Machine CT-01 calibrated successfully.",
        source="Scanner"
    )

    client = Client()
    
    print("Testing GET /api/admincenter/logs/")
    response = client.get('/api/admincenter/logs/')
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data}\n")
        assert len(data) == 2
        
        # Verify fields map to list_item_compliance.xml
        record = data[0]
        assert 'level' in record # Maps to compliance_title_text
        assert 'message' in record # Maps to compliance_desc_text
        assert 'timestamp' in record # Maps to compliance_time_text
        
        print("All compliance list item tests passed successfully!")
    else:
        print(f"Response: {response.content}\n")
        assert False, "admincenter API call failed"

if __name__ == "__main__":
    run_tests()
