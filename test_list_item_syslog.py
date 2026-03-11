import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.test import Client
from admincenter.models import SystemLog

def run_tests():
    SystemLog.objects.all().delete()
    
    # Create test log entries
    SystemLog.objects.create(level="INFO", message="Generated annual compliance report.", source="Admin User (Sarah)")
    SystemLog.objects.create(level="WARNING", message="CT Scanner 01 required recalibration.", source="System Automation")

    client = Client()
    
    # Test fetching list
    print("Testing GET /api/admincenter/logs/")
    response = client.get('/api/admincenter/logs/')
    if response.status_code == 200:
        data = response.json()
        assert len(data) == 2
        
        record = data[0] # Should be the newest
        assert 'timestamp' in record # Maps to timestamp_text_view
        assert 'source' in record # Maps to user_text_view
        assert 'message' in record # Maps to action_text_view
        
        print("GET Request passed successfully! Fields match UI requirements.")
    else:
        print(f"Response: {response.content}\n")
        assert False, "admincenter API GET call failed"
        
    print("All list item system log tests passed successfully!")

if __name__ == "__main__":
    run_tests()
