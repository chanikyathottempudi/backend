import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def run_tests():
    User.objects.all().delete()
    
    # Create test user
    User.objects.create_user(username="jdoe", email="jdoe@example.com", password="password", first_name="John", last_name="Doe", is_staff=True)
    User.objects.create_user(username="asmith", email="asmith@example.com", password="password", first_name="Alice", last_name="Smith", is_staff=False)

    client = Client()
    
    # Test fetching list
    print("Testing GET /api/admincenter/users/")
    response = client.get('/api/admincenter/users/')
    if response.status_code == 200:
        data = response.json()
        assert len(data) == 2
        
        record = data[0] # The list is ordered by -date_joined, so Alice is likely first
        print(f"Sample User Record parsed: {record}")
        
        assert 'id' in record # Contributes to user_details "ID: 000"
        assert 'first_name' in record # Contributes to user_name together with last_name
        assert 'last_name' in record # Contributes to user_name
        assert 'is_staff' in record # Contributes to user_details "Role" logic
        
        print("GET Request passed successfully! Fields match UI requirements.")
    else:
        print(f"Response: {response.content}\n")
        assert False, "admincenter users API GET call failed"
        
    print("All list item user dynamic tests passed successfully!")

if __name__ == "__main__":
    run_tests()
