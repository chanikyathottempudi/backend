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
    print("Starting test_signup_activity.py...")
    
    # 1. Setup
    client = APIClient()
    test_email = "emily.carter@hospital.com"
    test_license = "1234567"
    
    print(f"Cleaning up existing user with email: {test_email} or username: {test_license}")
    User.objects.filter(email=test_email).delete()
    User.objects.filter(username=test_license).delete()
    
    # 2. Test Signup with fields from signup.xml
    print("\nTesting POST /api/admincenter/signup/ with Android signup fields...")
    signup_data = {
        "full_name": "Emily Carter",
        "license_number": test_license,
        "email": test_email,
        "role": "Radiologist"
    }
    
    response = client.post(
        '/api/admincenter/signup/',
        json.dumps(signup_data),
        content_type='application/json'
    )
    
    print(f"Response Status Code: {response.status_code}")
    assert response.status_code == 201, f"Expected 201 Created, got {response.status_code}"
    
    data = response.json()
    print("✓ Signup successful")
    
    # 3. Verify Database Objects
    print("\nVerifying database objects...")
    
    user = User.objects.get(username=test_license)
    print(f"✓ User object found: {user.username}")
    assert user.first_name == "Emily"
    assert user.last_name == "Carter"
    assert user.email == test_email
    print(f"✓ Full Name correctly split: {user.first_name} {user.last_name}")
    
    profile = UserProfile.objects.get(user=user)
    print(f"✓ UserProfile object found: {profile.employee_id} ({profile.role})")
    assert profile.employee_id == test_license
    assert profile.role == "Radiologist"

    print("\nAll tests passed! The Signup Backend now fully supports the Android app's signup.xml requirements. 🎉")

if __name__ == '__main__':
    try:
        run_test()
    except AssertionError as e:
        print(f"\n❌ Test Failed: {e}")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
