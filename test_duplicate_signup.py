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
    print("Starting duplicate signup test...")
    
    test_email = 'duplicate@hospital.com'
    test_license = 'DUP123'
    
    # Clean up
    User.objects.filter(username=test_license).delete()
    User.objects.filter(email=test_email).delete()
    
    client = APIClient()
    signup_data = {
        "full_name": "Duplicate Test",
        "license_number": test_license,
        "email": test_email,
        "role": "Radiologist",
        "password": "password123"
    }
    
    # 1. First signup
    print("\nFirst signup attempt...")
    response1 = client.post('/api/admincenter/signup/', signup_data, format='json')
    print(f"Status: {response1.status_code}")
    assert response1.status_code == 201
    
    # 2. Duplicate signup (same license number)
    print("\nSecond signup attempt with same license number...")
    response2 = client.post('/api/admincenter/signup/', signup_data, format='json')
    print(f"Status: {response2.status_code}")
    print(f"Body: {response2.content.decode()}")
    
    # 3. Duplicate signup (different license, same email)
    print("\nThird signup attempt with different license, same email...")
    signup_data2 = signup_data.copy()
    signup_data2["license_number"] = "DUP456"
    response3 = client.post('/api/admincenter/signup/', signup_data2, format='json')
    print(f"Status: {response3.status_code}")
    print(f"Body: {response3.content.decode()}")

if __name__ == '__main__':
    run_test()
