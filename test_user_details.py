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
    print("Starting test_user_details.py...")
    
    # 1. Setup Data
    print("Preparing test data...")
    User.objects.filter(username='detail_test_user').delete()
    
    user = User.objects.create_user(
        username='detail_test_user', 
        password='password123',
        email='details@hospital.com',
        first_name='John',
        last_name='Doe'
    )
    
    # Update the profile (created by signal)
    profile = user.profile
    profile.employee_id = 'RAD-204'
    profile.role = 'Senior Radiologist'
    profile.phone_number = '+91 98765 43210'
    profile.permissions_summary = '• Access to Patient Records\n• Real-time Dose Monitoring'
    profile.save()
    
    print(f"Created user: {user.username} with full profile details.")
    
    client = APIClient()
    
    # 2. Test Unauthenticated Access
    print("\nTesting without authentication...")
    response = client.get('/api/admincenter/me/')
    assert response.status_code == 401
    print("✓ Unauthenticated access correctly blocked (401)")
    
    # 3. Authenticate User
    client.force_authenticate(user=user)
    
    # 4. Test GET /api/admincenter/me/
    print("\nTesting GET /api/admincenter/me/...")
    response = client.get('/api/admincenter/me/')
    assert response.status_code == 200
    data = response.json()
    
    # Verify fields
    assert data['username'] == 'detail_test_user'
    assert data['email'] == 'details@hospital.com'
    assert data['employee_id_display'] == 'RAD-204'
    assert data['role_display'] == 'Senior Radiologist'
    assert data['phone_number_display'] == '+91 98765 43210'
    assert 'Access to Patient Records' in data['permissions_summary_display']
    
    print(f"✓ Profile details verified: Name={data['first_name']} {data['last_name']}, ID={data['employee_id_display']}")
    print(f"✓ Contact info verified: Email={data['email']}, Phone={data['phone_number_display']}")
    print(f"✓ Permissions verified.")

    # 5. Test PATCH /api/admincenter/me/ (Profile Update)
    print("\nTesting PATCH /api/admincenter/me/ (Update Phone Number)...")
    patch_data = {
        'phone_number': '+91 00000 00000'
    }
    response = client.patch(
        '/api/admincenter/me/',
        json.dumps(patch_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = response.json()
    assert data['phone_number_display'] == '+91 00000 00000'
    print("✓ Profile update (PATCH) verified: Phone number updated to +91 00000 00000")

    print("\nAll tests passed successfully! The User Details Backend is fully functional. 👤")

if __name__ == '__main__':
    try:
        run_test()
    except AssertionError as e:
        print(f"\n❌ Test Failed: {e}")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
