import os
import django
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from rest_framework.test import APIClient
from django.contrib.auth.models import User

def run_test():
    client = APIClient()
    
    # 1. Check if user exists or create
    username = "1234567"
    email = "emily.carter@hospital.com"
    password = "securepassword123"
    
    User.objects.filter(username=username).delete()
    User.objects.create_user(username=username, email=email, password=password)
    
    # 2. Try login with WRONG password
    print(f"Testing login for {username} with WRONG password...")
    data = {
        "username": username,
        "password": "wrong-password-123"
    }
    
    response = client.post('/api/doctor/login/', data, format='json')
    print(f"Response Status: {response.status_code}")
    print(f"Response Data: {response.data}")
    
    if response.status_code == 200:
        print("!!! SECURITY ALERT: Login succeeded with wrong password !!!")
    else:
        print("✓ Login failed with wrong password as expected.")

if __name__ == '__main__':
    run_test()
