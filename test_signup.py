import os
import django
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from rest_framework.test import APIClient
from django.contrib.auth.models import User
from admincenter.models import UserProfile, SecuritySettings

def run_test():
    print("Starting test_signup.py...")
    
    # 1. Setup
    print("Cleaning up existing test data...")
    User.objects.filter(email='emily.carter@hospital.com').delete()
    User.objects.filter(username='1234567').delete() # employee_id becomes username
    
    client = APIClient()
    
    # 2. Test Signup with valid data
    print("\nTesting POST /api/admincenter/signup/ with valid signup data...")
    signup_data = {
        "first_name": "Emily",
        "last_name": "Carter",
        "email": "emily.carter@hospital.com",
        "employee_id": "1234567",
        "role": "Radiologist",
        "password": "securepassword123"
    }
    
    response = client.post(
        '/api/admincenter/signup/',
        json.dumps(signup_data),
        content_type='application/json'
    )
    
    print(f"POST Response Status Code: {response.status_code}")
    assert response.status_code == 201, f"Expected 201 Created, got {response.status_code}"
    
    response_data = response.json()
    print(f"Response Data:\n{json.dumps(response_data, indent=2)}")
    
    # Verify response contains the expected fields
    assert response_data['email'] == "emily.carter@hospital.com"
    assert response_data['first_name'] == "Emily"
    assert response_data['last_name'] == "Carter"
    
    # 3. Verify Database Objects
    print("\nQuerying Database for newly created objects...")
    
    # Verify User
    user = User.objects.get(username="1234567")
    print(f"✓ Found User object: {user.username}")
    assert user.email == "emily.carter@hospital.com"
    
    # Verify Profile
    profile = UserProfile.objects.get(user=user)
    print(f"✓ Found UserProfile object: {profile.employee_id} ({profile.role})")
    assert profile.employee_id == "1234567"
    assert profile.role == "Radiologist"
    
    # Verify Settings (via signal)
    settings = SecuritySettings.objects.get(user=user)
    print(f"✓ Found SecuritySettings object: {settings}")
    assert settings.biometric_login == False # default
    assert settings.data_encryption == True # default
    
    # 4. Test Error Handling (Missing Role)
    print("\nTesting POST /api/admincenter/signup/ with missing requires fields...")
    invalid_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@hospital.com",
        # Missing employee_id
        # Missing role
        "password": "password123"
    }
    
    response = client.post(
        '/api/admincenter/signup/',
        json.dumps(invalid_data),
        content_type='application/json'
    )
    
    assert response.status_code == 400, f"Expected 400 Bad Request, got {response.status_code}"
    error_data = response.json()
    assert 'employee_id' in error_data
    assert 'role' in error_data
    print("✓ Missing fields correctly rejected (400)")
    
    print("\nAll tests passed successfully! The Dedicated Signup Backend endpoint fully supports the Android app requirements. 🎉")

if __name__ == '__main__':
    try:
        run_test()
    except AssertionError as e:
        print(f"\n❌ Test Failed: {e}")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
