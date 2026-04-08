import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User

def check_user():
    identifier = 'chanikya123@gmail.com'
    print(f"SEARCHING FOR: {identifier}")
    
    # 1. Search by email
    user_by_email = User.objects.filter(email=identifier).first()
    if user_by_email:
        print(f"FOUND BY EMAIL: username='{user_by_email.username}', email='{user_by_email.email}', id={user_by_email.id}")
    else:
        print("NOT FOUND BY EMAIL")
        
    # 2. Search by username
    user_by_username = User.objects.filter(username=identifier).first()
    if user_by_username:
        print(f"FOUND BY USERNAME: username='{user_by_username.username}', email='{user_by_username.email}', id={user_by_username.id}")
    else:
        print("NOT FOUND BY USERNAME")

    # 3. Check profile
    if user_by_email or user_by_username:
        u = user_by_email or user_by_username
        if hasattr(u, 'profile'):
            print(f"PROFILE ROLE: {u.profile.role}")
            print(f"PROFILE ADMIN: {u.profile.role.lower() == 'hospital admin'}")
        else:
            print("NO PROFILE FOUND")

if __name__ == '__main__':
    check_user()
