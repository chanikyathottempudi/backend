import os
import django
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def run_test():
    print("Starting test_reset_password.py...")
    
    # 1. Setup Test Data
    print("Cleaning up existing test data...")
    User.objects.filter(username='reset_test_user').delete()
    
    # Create the test user
    user = User.objects.create_user(
        username='reset_test_user', 
        password='old_password123',
        email='reset@test.com'
    )
    print(f"Created user: {user.username} with initial password.")
    
    client = APIClient()
    
    # 2. Test Unauthenticated Access
    print("\nTesting without authentication...")
    response = client.post(
        '/api/admincenter/reset-password/',
        json.dumps({'new_password': 'newpassword123', 'repeat_password': 'newpassword123'}),
        content_type='application/json'
    )
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"
    print("✓ Unauthenticated access correctly blocked (401)")
    
    # 3. Authenticate User
    client.force_authenticate(user=user)
    
    # 4. Test Mismatched Passwords
    print("\nTesting POST with mismatched passwords...")
    mismatched_data = {
        'new_password': 'newpassword123',
        'repeat_password': 'differentpassword'
    }
    response = client.post(
        '/api/admincenter/reset-password/',
        json.dumps(mismatched_data),
        content_type='application/json'
    )
    assert response.status_code == 400, f"Expected 400 Bad Request, got {response.status_code}"
    print("✓ Mismatched passwords correctly rejected (400)")
    
    # 5. Test Short Passwords
    print("\nTesting POST with passwords under 8 characters...")
    short_data = {
        'new_password': 'short',
        'repeat_password': 'short'
    }
    response = client.post(
        '/api/admincenter/reset-password/',
        json.dumps(short_data),
        content_type='application/json'
    )
    assert response.status_code == 400, f"Expected 400 Bad Request, got {response.status_code}"
    print("✓ Short passwords correctly rejected (400)")
    
    # 6. Test Valid Password Reset
    print("\nTesting POST /api/admincenter/reset-password/ with valid, matching passwords...")
    valid_data = {
        'new_password': 'SuperNewPassword2026!',
        'repeat_password': 'SuperNewPassword2026!'
    }
    response = client.post(
        '/api/admincenter/reset-password/',
        json.dumps(valid_data),
        content_type='application/json'
    )
    
    print(f"POST Response Status Code: {response.status_code}")
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    
    response_data = response.json()
    print(f"Response Message: {response_data.get('message')}")
    assert response_data.get('message') == "Password successfully reset."
    print("✓ API confirmed successful reset (200)")
    
    # 7. Verify Database Authentication
    print("\nVerifying database authentication with new password...")
    # Refresh user from database
    user.refresh_from_db()
    
    # Verify the OLD password fails
    auth_old = authenticate(username='reset_test_user', password='old_password123')
    assert auth_old is None, "Old password surprisingly still works!"
    print("✓ Old password no longer authenticates.")
    
    # Verify the NEW password succeeds
    auth_new = authenticate(username='reset_test_user', password='SuperNewPassword2026!')
    assert auth_new is not None, "New password failed to authenticate!"
    assert auth_new.username == 'reset_test_user'
    print("✓ New password successfully authenticates user object.")

    print("\nAll tests passed successfully! The Reset Password Backend is fully functional. 🔐")

if __name__ == '__main__':
    try:
        run_test()
    except AssertionError as e:
        print(f"\n❌ Test Failed: {e}")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
