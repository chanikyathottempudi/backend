import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.test import Client

def run_tests():
    client = Client()
    
    # Test valid forgot password request
    print("Testing POST /api/doctor/forgot-password/ with email")
    response = client.post('/api/doctor/forgot-password/', {'email': 'test@example.com'})
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}\n")
    else:
        print(f"Response: {response.content}\n")
        assert False, "Valid email forgot password failed"

    # Test missing email
    print("Testing POST /api/doctor/forgot-password/ without email")
    response_missing = client.post('/api/doctor/forgot-password/', {})
    print(f"Status Code: {response_missing.status_code}")
    if response_missing.status_code == 400:
        print(f"Response: {response_missing.json()}\n")
    else:
        print(f"Response: {response_missing.content}\n")
        assert False, "Missing email validation failed"

    print("All forgotten password tests passed successfully!")

if __name__ == "__main__":
    run_tests()
