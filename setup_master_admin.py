import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from admincenter.models import UserProfile

def setup_admin():
    admin_id = "Admin999"
    admin_pass = "Admin@Simats2026"
    admin_email = "admin@simats.com"
    
    print(f"Setting up Master Admin: {admin_id}")
    
    # Delete existing if any
    User.objects.filter(username=admin_id).delete()
    User.objects.filter(email=admin_email).delete()
    
    # Create User
    user = User.objects.create_user(
        username=admin_id,
        email=admin_email,
        password=admin_pass,
        first_name="Master",
        last_name="Admin"
    )
    
    # Create Profile with Admin role
    UserProfile.objects.create(
        user=user,
        employee_id=admin_id,
        role="Admin"
    )
    
    print(f"✓ Master Admin '{admin_id}' created successfully with password '{admin_pass}'")

if __name__ == '__main__':
    setup_admin()
