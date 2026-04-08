import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from admincenter.models import UserProfile

def fix_user():
    email = 'chanikya123@gmail.com'
    password = '12345'
    role = 'Hospital Admin'
    employee_id = 'chanikya123'
    
    print(f"Finding user with email {email}...")
    user = User.objects.filter(email=email).first()
    
    if not user:
        print(f"User not found! Creating user {employee_id}...")
        user = User.objects.create_user(username=employee_id, email=email, password=password)
    else:
        print(f"User found: {user.username}. Resetting password...")
        user.set_password(password)
        user.save()
    
    print(f"Setting up profile for {user.username} with role '{role}'...")
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={'employee_id': employee_id, 'role': role}
    )
    
    if not created:
        profile.role = role
        profile.employee_id = employee_id
        profile.save()
        
    print(f"SUCCESS: User {user.username} is now ready with role '{role}' and password '{password}'")

if __name__ == '__main__':
    fix_user()
