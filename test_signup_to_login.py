import os
import django
import json
import secrets

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from rest_framework.test import APIClient
from django.contrib.auth.models import User
from admincenter.models import UserProfile

def run_test():
    print("Starting test_signup_to_login.py...")
    
    client = APIClient()
    
    # Generate unique test data
    unique_id = f"LV{secrets.token_hex(3)}"
    test_email = f"test_{secrets.token_hex(2)}@hospital.com"
    full_name = "Dynamic User"
    
    print(f"Test Details: ID={unique_id}, Email={test_email}")

    # 1. SIGNUP
    print("\n[STAGING 1] Signing up...")
    signup_data = {
        "full_name": full_name,
        "license_number": unique_id,
        "email": test_email,
        "role": "CT Technician"
    }
    
    response = client.post(
        '/admincenter/signup/',
        json.dumps(signup_data),
        content_type='application/json'
    )
    
    assert response.status_code == 201, f"Signup failed: {response.status_code} {response.data}"
    print("✓ Signup successful")

    # 2. LOGIN (Using ID as password)
    print(f"\n[STAGING 2] Logging in with ID: {unique_id} and Password: {unique_id}")
    login_data = {
        "username": unique_id,
        "password": unique_id
    }
    
    response = client.post(
        '/doctor/login/',
        json.dumps(login_data),
        content_type='application/json'
    )
    
    assert response.status_code == 200, f"Login failed: {response.status_code} {response.data}"
    data = response.json()
    print("✓ Login successful!")
    assert data['success'] is True
    assert data['user']['employee_id'] == unique_id
    assert data['user']['role'] == "CT Technician"

    print("\n[VERIFICATION] Final flow Signup -> Login (Dynamic) is WORKING. 🎉")

if __name__ == '__main__':
    try:
        run_test()
    except AssertionError as e:
        print(f"\n❌ Test Failed: {e}")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
