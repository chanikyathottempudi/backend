import os
import django
import json
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from rest_framework.test import APIClient
from django.contrib.auth.models import User
from admincenter.models import UserProfile

def run_test():
    print("Starting signup reproduction test...")
    
    # 1. Setup
    test_email = 'test.failure@hospital.com'
    test_license = 'FAIL999'
    
    User.objects.filter(email=test_email).delete()
    User.objects.filter(username=test_license).delete()
    
    client = APIClient()
    
    # 2. Test Signup with data exactly like Android app sends
    # com.simats.finalapp.model.SignupRequest uses:
    # fullName, licenseNumber, email, role, password
    # UserSerializer in admincenter/serializers.py expects:
    # full_name, license_number, email, role, password
    
    print("\nTesting POST /api/admincenter/signup/ with Android-style data...")
    signup_data = {
        "full_name": "Test Failure",
        "license_number": test_license,
        "email": test_email,
        "role": "Radiologist",
        "password": "password123"
    }
    
    response = client.post(
        '/api/admincenter/signup/',
        data=signup_data, # Use data= for multipart/form-data or dict-like submission
        format='json'
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code != 201:
        print(f"Error Response: {response.content.decode()}")
        return

    print("Signup successful in test!")
    
    # Verify User
    try:
        user = User.objects.get(username=test_license)
        print(f"User created: {user.username}")
        profile = UserProfile.objects.get(user=user)
        print(f"Profile created with role: {profile.role}")
    except Exception as e:
        print(f"Verification failed: {str(e)}")

if __name__ == '__main__':
    run_test()
