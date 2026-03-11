import os
import django
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from admincenter.models import SecuritySettings

def run_test():
    print("Starting test_security_settings.py...")
    
    # 1. Setup Data
    print("Setting up test user...")
    # Clean up existing to ensure repeatable tests
    User.objects.filter(username='sec_test_user').delete()
    
    # Creating a user should automatically trigger the signal to create SecuritySettings
    user = User.objects.create_user(username='sec_test_user', password='testpassword123')
    print(f"Created user: {user.username}")
    
    # Verify the signal worked
    settings = SecuritySettings.objects.get(user=user)
    print(f"Auto-created settings for user: {settings}")
    assert settings.biometric_login == False, "Default biometric_login should be False"
    assert settings.data_encryption == True, "Default data_encryption should be True"
    assert settings.automatic_logout == True, "Default automatic_logout should be True"
    assert settings.hipaa_compliance == True, "Default hipaa_compliance should be True"
    
    client = Client()
    
    # Try accessing without authentication
    response = client.get('/api/admincenter/security-settings/')
    assert response.status_code == 200, f"Expected 200 for unauthenticated GET, got {response.status_code}"
    assert len(response.json()) == 0, "Unauthenticated users should see 0 settings"
    
    # 2. Test the API Endpoints (Authenticated)
    print("\nTesting GET /api/admincenter/security-settings/ (Authenticated)...")
    client.login(username='sec_test_user', password='testpassword123')
    response = client.get('/api/admincenter/security-settings/')
    
    # 3. Assertions
    print(f"Response Status Code: {response.status_code}")
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    response_data = response.json()
    print(f"Response Data:\n{json.dumps(response_data, indent=2)}")
    
    assert len(response_data) == 1, f"Expected 1 settings object, got {len(response_data)}"
    
    returned_settings = response_data[0]
    settings_id = returned_settings['id']
    
    # 4. Test Updating (PATCH)
    print("\nTesting PATCH /api/admincenter/security-settings/{id}/...")
    update_data = {
        'biometric_login': True,
        'hipaa_compliance': False
    }
    
    response = client.patch(
        f'/api/admincenter/security-settings/{settings_id}/', 
        json.dumps(update_data),
        content_type='application/json'
    )
    
    print(f"PATCH Response Status Code: {response.status_code}")
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    updated_data = response.json()
    print(f"Updated Data:\n{json.dumps(updated_data, indent=2)}")
    
    assert updated_data['biometric_login'] == True, "biometric_login should be True after update"
    assert updated_data['hipaa_compliance'] == False, "hipaa_compliance should be False after update"
    assert updated_data['data_encryption'] == True, "data_encryption should remain unchanged"
    
    print("\nAll tests passed successfully! The Security Settings Backend is fully functional. 🔒")

if __name__ == '__main__':
    try:
        run_test()
    except AssertionError as e:
        print(f"\n❌ Test Failed: {e}")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
