import os
import django
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from rest_framework.test import APIClient
from django.contrib.auth.models import User
from admincenter.models import UserProfile

def run_test():
    print("Starting test_user_management.py...")
    
    # 1. Setup Data
    print("Preparing test data...")
    # Clean up
    User.objects.filter(username__startswith='mgt_test_user').delete()
    
    # Create multiple users with profiles
    users_data = [
        {'username': 'mgt_test_user1', 'first_name': 'Aris', 'last_name': 'Thorne', 'employee_id': 'RAD-204', 'role': 'Senior Radiologist'},
        {'username': 'mgt_test_user2', 'first_name': 'Sarah', 'last_name': 'Jenkins', 'employee_id': 'TEC-882', 'role': 'Lead Technician'},
        {'username': 'mgt_test_user3', 'first_name': 'Marcus', 'last_name': 'Vane', 'employee_id': 'TEC-104', 'role': 'CT Technician'},
    ]
    
    for u in users_data:
        user = User.objects.create_user(
            username=u['username'],
            password='password123',
            first_name=u['first_name'],
            last_name=u['last_name']
        )
        # Profile is created by signal, just update it
        profile = user.profile
        profile.employee_id = u['employee_id']
        profile.role = u['role']
        profile.save()
        
    # Create 10 more users for pagination
    for i in range(10):
        uname = f'mgt_test_user_pag_{i}'
        user = User.objects.create_user(username=uname, password='p')
        profile = user.profile
        profile.employee_id = f'PAG-{i}'
        profile.role = 'Technician'
        profile.save()

    print(f"Created {len(users_data) + 10} test users with profiles.")
    
    client = APIClient()
    # No authentication required for these tests as per current viewset (it has no permission_classes explicitly set to IsAuthenticated)
    
    # 2. Test Pagination
    print("\nTesting pagination on /api/admincenter/users/...")
    response = client.get('/api/admincenter/users/')
    assert response.status_code == 200
    data = response.json()
    assert 'results' in data
    assert 'count' in data
    assert data['count'] >= 13
    assert len(data['results']) == 10 # standard results set size
    print(f"✓ Pagination verified: {data['count']} total users found.")

    # 3. Test Search by Name
    print("\nTesting search by name (?search=Thorne)...")
    response = client.get('/api/admincenter/users/?search=Thorne')
    assert response.status_code == 200
    data = response.json()
    assert data['count'] == 1
    assert data['results'][0]['first_name'] == 'Aris'
    print(f"✓ Search by name verified: found {data['results'][0]['first_name']} {data['results'][0]['last_name']}")

    # 4. Test Search by Employee ID
    print("\nTesting search by Employee ID (?search=TEC-882)...")
    response = client.get('/api/admincenter/users/?search=TEC-882')
    assert response.status_code == 200
    data = response.json()
    assert data['count'] == 1
    assert data['results'][0]['employee_id_display'] == 'TEC-882'
    print(f"✓ Search by Employee ID verified: found user with ID {data['results'][0]['employee_id_display']}")

    # 5. Test Search by Role
    print("\nTesting search by Role (?search=Radiologist)...")
    response = client.get('/api/admincenter/users/?search=Radiologist')
    assert response.status_code == 200
    data = response.json()
    assert data['count'] == 1
    assert data['results'][0]['role_display'] == 'Senior Radiologist'
    print(f"✓ Search by Role verified: found {data['results'][0]['role_display']}")

    print("\nAll tests passed successfully! The User Management Backend is fully functional. 👥")

if __name__ == '__main__':
    try:
        run_test()
    except AssertionError as e:
        print(f"\n❌ Test Failed: {e}")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
