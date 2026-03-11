import os
import django
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from rest_framework.test import APIClient
from django.contrib.auth.models import User
from admincenter.models import SystemLog

def run_test():
    print("Starting test_system_logs.py...")
    
    # 1. Setup Data
    print("Preparing test data...")
    SystemLog.objects.all().delete()
    User.objects.filter(username__startswith='testloguser').delete()
    
    user1 = User.objects.create_user(username='testloguser1', password='password')
    user2 = User.objects.create_user(username='testloguser2', password='password')
    
    # Create 15 logs to trigger pagination (page_size=10)
    for i in range(15):
        SystemLog.objects.create(
            level='INFO',
            message=f'Log message {i}',
            source='Auth',
            user=user1 if i < 10 else user2
        )
    print("Created 2 users and 15 test logs.")
    
    client = APIClient()
    
    # 2. Test Pagination
    print("\nTesting pagination on /api/admincenter/logs/...")
    response = client.get('/api/admincenter/logs/')
    assert response.status_code == 200
    data = response.json()
    
    # Check for DRF pagination structure
    assert 'count' in data
    assert 'next' in data
    assert 'results' in data
    assert data['count'] == 15
    assert len(data['results']) == 10 # Page 1 size
    print(f"✓ Pagination verified: count={data['count']}, results on page 1={len(data['results'])}")
    
    # 3. Test Search
    print("\nTesting search filter (?search=testloguser2)...")
    response = client.get('/api/admincenter/logs/?search=testloguser2')
    assert response.status_code == 200
    data = response.json()
    
    # Only logs 10-14 were assigned to user2
    assert data['count'] == 5
    for result in data['results']:
        assert result['user_display'] == 'testloguser2'
    print(f"✓ Search filter verified: found {data['count']} logs for testloguser2")
    
    # Test searching in message
    print("\nTesting search filter in message (?search=message 7)...")
    response = client.get('/api/admincenter/logs/?search=message 7')
    assert response.status_code == 200
    data = response.json()
    assert data['count'] == 1
    assert 'message 7' in data['results'][0]['message']
    print(f"✓ Search by message content verified: found {data['count']} log")

    print("\nAll tests passed successfully! The System Logs Backend is fully functional. 📜")

if __name__ == '__main__':
    try:
        run_test()
    except AssertionError as e:
        print(f"\n❌ Test Failed: {e}")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
