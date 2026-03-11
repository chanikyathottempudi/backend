import os
import django
import json
import secrets

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.test import APIClient

def run_debug_test():
    client = APIClient()
    
    # 1. Create a fresh test user
    username = f"debug_user_{secrets.token_hex(4)}"
    password = "correct_password_123"
    User.objects.create_user(username=username, password=password)
    
    print(f"\n--- DEBUG TEST for {username} ---")
    
    # 2. Test with WRONG password
    print("Testing with WRONG password...")
    response = client.post('/api/doctor/login/', {'username': username, 'password': 'WRONG_PASSWORD'}, format='json')
    print(f"Status: {response.status_code}")
    print(f"Body: {response.data}")
    
    # 3. Test with CORRECT password
    print("\nTesting with CORRECT password...")
    response = client.post('/api/doctor/login/', {'username': username, 'password': password}, format='json')
    print(f"Status: {response.status_code}")
    # print(f"Body: {response.data}") # Don't print tokens for safety
    
    print("\n--- END DEBUG TEST ---")

if __name__ == '__main__':
    run_debug_test()
