import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from admincenter.models import UserProfile

def setup_secure_user():
    print("Cleaning up all existing test users...")
    # Delete users that might have been created during testing
    User.objects.filter(username__in=['1234567', '88888', '99999', 'admin']).delete()
    
    # Create the secure user
    username = "88888"
    email = "admin@hospital.com"
    password = "Secure@Login123"
    
    print(f"Creating secure user: {username} ...")
    user = User.objects.create_user(
        username=username, 
        email=email, 
        password=password,
        first_name="Secure",
        last_name="Admin"
    )
    
    # Create profile
    UserProfile.objects.get_or_create(
        user=user,
        defaults={
            'employee_id': username,
            'role': "Hospital Admin"
        }
    )
    
    # Verify authentication in-script
    from django.contrib.auth import authenticate
    auth_success = authenticate(username=username, password=password)
    auth_fail = authenticate(username=username, password="wrongpassword")
    
    print(f"Verification - Correct password: {'PASSED' if auth_success else 'FAILED'}")
    print(f"Verification - Wrong password: {'PASSED (Rejected)' if not auth_fail else 'FAILED (Accepted)'}")
    
    if auth_success and not auth_fail:
        print("\n--- SECURE CREDENTIALS ---")
        print(f"Employee ID: {username}")
        print(f"Email:       {email}")
        print(f"Password:    {password}")
        print("--------------------------")
    else:
        print("!!! ERROR: Authentication still behave unexpectedly in script !!!")

if __name__ == '__main__':
    setup_secure_user()
