import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User

def check_users():
    users = User.objects.all()
    print(f"{'Username':<20} | {'Has Password?':<15} | {'Is Active?':<10}")
    print("-" * 50)
    for user in users:
        has_usable = user.has_usable_password()
        print(f"{user.username:<20} | {str(has_usable):<15} | {str(user.is_active):<10}")

if __name__ == '__main__':
    check_users()
