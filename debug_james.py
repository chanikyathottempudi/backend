import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from admincenter.models import UserProfile, SecuritySettings
from rest_framework.test import APIClient

def diagnose():
    email = 'james.wilson@hospital.com'
    username = email[:50]
    
    print(f"Diagnosing for {email} / {username}")
    
    # 1. Check existing
    users = User.objects.filter(models.Q(email=email) | models.Q(username=username))
    print(f"Found {users.count()} users.")
    for u in users:
        print(f"User: {u.username}, Email: {u.email}")
        
    profiles = UserProfile.objects.filter(employee_id=username)
    print(f"Found {profiles.count()} profiles with employee_id {username}")
    
    # 2. Cleanup
    User.objects.filter(email=email).delete()
    User.objects.filter(username=username).delete()
    UserProfile.objects.filter(employee_id=username).delete()
    print("Cleanup done.")
    
    # 3. Test Signup
    client = APIClient()
    signup_data = {
        "full_name": "James Wilson",
        "email": email,
        "role": "CT Technician",
        "password": "techpassword789"
    }
    
    response = client.post('/api/admincenter/signup/', signup_data, format='json')
    print(f"Status Code: {response.status_code}")
    if response.status_code != 201:
        print(f"Error: {response.data}")
    else:
        print("Signup Successful!")

if __name__ == '__main__':
    from django.db import models
    diagnose()
