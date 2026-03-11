import os
import django
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.test import Client
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from admincenter.models import UserProfile

def run_test():
    print("Starting test_select_role.py...")
    
    # 1. Setup Data
    print("Setting up test user and profile...")
    # Clean up existing to ensure repeatable tests
    User.objects.filter(username='role_test_user').delete()
    
    user = User.objects.create_user(username='role_test_user', password='testpassword123')
    UserProfile.objects.create(user=user, employee_id='EMP999', role='Pending')
    print(f"Created user: {user.username} with initial role: 'Pending'")
    
    client = APIClient()
    
    # Try accessing without authentication
    print("\nTesting without authentication...")
    response = client.patch(
        '/api/admincenter/select-role/',
        json.dumps({'role': 'Radiologist'}),
        content_type='application/json'
    )
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"
    print("✓ Unauthenticated access correctly blocked (401)")
    
    # Login
    client.force_authenticate(user=user)
    
    # 2. Test Invalid Role
    print("\nTesting PATCH with invalid role...")
    response = client.patch(
        '/api/admincenter/select-role/',
        json.dumps({'role': 'Hacker'}),
        content_type='application/json'
    )
    assert response.status_code == 400, f"Expected 400 Bad Request, got {response.status_code}"
    print("✓ Invalid role correctly rejected (400)")
    
    # 3. Test Valid Role Update
    print("\nTesting PATCH /api/admincenter/select-role/ with 'Radiologist'...")
    response = client.patch(
        '/api/admincenter/select-role/',
        json.dumps({'role': 'Radiologist'}),
        content_type='application/json'
    )
    
    print(f"PATCH Response Status Code: {response.status_code}")
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    response_data = response.json()
    print(f"Response Data:\n{json.dumps(response_data, indent=2)}")
    
    # 4. Verify Database Update
    user.profile.refresh_from_db()
    assert user.profile.role == 'Radiologist', f"Expected role in DB to be 'Radiologist', got '{user.profile.role}'"
    print("✓ Database successfully updated to 'Radiologist'")
    
    # Test another valid role
    print("\nTesting PATCH with 'CT Technician'...")
    response = client.patch(
        '/api/admincenter/select-role/',
        json.dumps({'role': 'CT Technician'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    user.profile.refresh_from_db()
    assert user.profile.role == 'CT Technician'
    print("✓ Database successfully updated to 'CT Technician'")
    
    print("\nAll tests passed successfully! The Select Role Backend is fully functional. 🎯")

if __name__ == '__main__':
    try:
        run_test()
    except AssertionError as e:
        print(f"\n❌ Test Failed: {e}")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
