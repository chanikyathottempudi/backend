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
    print("Starting test_login_slide.py...")
    
    # 1. Setup - Create a test user if it doesn't exist
    print("Setting up test user...")
    test_username = "1234567"
    test_email = "emily.carter@hospital.com"
    test_password = "securepassword123"
    
    # Clean up existing test data
    User.objects.filter(username=test_username).delete()
    User.objects.filter(email=test_email).delete()
    
    user = User.objects.create_user(
        username=test_username,
        email=test_email,
        password=test_password,
        first_name="Emily",
        last_name="Carter"
    )
    
    # Create profile
    UserProfile.objects.create(
        user=user,
        employee_id=test_username,
        role="Radiologist"
    )
    
    client = APIClient()
    
    # 2. Test Login with Email
    print(f"\nTesting Login with Email: {test_email}")
    login_data_email = {
        "username": test_email,
        "password": test_password
    }
    
    response = client.post(
        '/api/doctor/login/',
        json.dumps(login_data_email),
        content_type='application/json'
    )
    
    print(f"Response Status Code: {response.status_code}")
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    
    data = response.json()
    print("✓ Login with email successful")
    assert 'access' in data
    assert data['user']['email'] == test_email
    assert data['user']['employee_id'] == test_username
    assert data['user']['role'] == "Radiologist"

    # 3. Test Login with Employee ID (Username)
    print(f"\nTesting Login with Employee ID: {test_username}")
    login_data_id = {
        "username": test_username,
        "password": test_password
    }
    
    response = client.post(
        '/api/doctor/login/',
        json.dumps(login_data_id),
        content_type='application/json'
    )
    
    print(f"Response Status Code: {response.status_code}")
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    
    data = response.json()
    print("✓ Login with employee ID successful")
    assert 'access' in data
    assert data['user']['employee_id'] == test_username

    # 4. Test Login with Incorrect Password
    print("\nTesting Login with Incorrect Password...")
    invalid_password_data = {
        "username": test_email,
        "password": "wrongpassword"
    }
    
    response = client.post(
        '/api/doctor/login/',
        json.dumps(invalid_password_data),
        content_type='application/json'
    )
    
    print(f"Response Status Code: {response.status_code}")
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"
    print("✓ Incorrect password correctly rejected")

    # 5. Test Login with Non-existent User
    print("\nTesting Login with Non-existent User...")
    non_existent_data = {
        "username": "nonexistent@hospital.com",
        "password": test_password
    }
    
    response = client.post(
        '/api/doctor/login/',
        json.dumps(non_existent_data),
        content_type='application/json'
    )
    
    print(f"Response Status Code: {response.status_code}")
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"
    print("✓ Non-existent user correctly rejected")

    print("\nAll tests passed successfully! The Login Backend fully supports the Android app's Login Slide requirements. 🎉")

if __name__ == '__main__':
    try:
        run_test()
    except AssertionError as e:
        print(f"\n❌ Test Failed: {e}")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
