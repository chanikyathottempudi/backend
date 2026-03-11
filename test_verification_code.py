import os
import django
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from rest_framework.test import APIClient
from django.contrib.auth.models import User
from admincenter.models import VerificationCode

def run_test():
    print("Starting test_verification_code.py...")
    
    # 1. Setup Data
    print("Preparing test data...")
    User.objects.filter(username='verify_test_user').delete()
    user = User.objects.create_user(
        username='verify_test_user', 
        password='password123',
        email='verify@hospital.com'
    )
    print(f"Created user: {user.username} (Email: {user.email})")
    
    client = APIClient()
    
    # 2. Test Send Verification Code
    print("\nTesting /api/admincenter/send-verification/...")
    response = client.post('/api/admincenter/send-verification/', {'email': 'verify@hospital.com'}, format='json')
    assert response.status_code == 200
    data = response.json()
    assert 'code' in data
    code = data['code']
    print(f"✓ Verification code generated and received: {code}")
    
    # Verify in DB
    db_code = VerificationCode.objects.filter(user=user, code=code).first()
    assert db_code is not None
    print("✓ Code verified in database.")
    
    # 3. Test Verify Code (Correct Code)
    print("\nTesting /api/admincenter/verify-code/ (Correct Code)...")
    response = client.post('/api/admincenter/verify-code/', {'email': 'verify@hospital.com', 'code': code}, format='json')
    assert response.status_code == 200
    print("✓ Verification successful response received.")
    
    # Verify DB status
    db_code.refresh_from_db()
    assert db_code.is_verified == True
    print("✓ is_verified updated to True in database.")
    
    # 4. Test Verify Code (Incorrect Code)
    print("\nTesting /api/admincenter/verify-code/ (Incorrect Code)...")
    response = client.post('/api/admincenter/verify-code/', {'email': 'verify@hospital.com', 'code': '000000'}, format='json')
    assert response.status_code == 400
    print("✓ Incorrect code correctly rejected.")
    
    # 5. Test Send Code to Non-existent Email
    print("\nTesting /api/admincenter/send-verification/ with non-existent email...")
    response = client.post('/api/admincenter/send-verification/', {'email': 'nonexistent@hospital.com'}, format='json')
    assert response.status_code == 404
    print("✓ Non-existent email correctly handled (404).")

    print("\nAll tests passed successfully! The Verification Code Backend is fully functional. 🔐")

if __name__ == '__main__':
    try:
        run_test()
    except AssertionError as e:
        print(f"\n❌ Test Failed: {e}")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
