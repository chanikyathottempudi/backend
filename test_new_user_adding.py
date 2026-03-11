import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from rest_framework.test import APIClient
from django.contrib.auth.models import User
from admincenter.models import UserProfile
from django.core.files.uploadedfile import SimpleUploadedFile

def run_tests():
    client = APIClient()

    print("--- Testing New User Profile Creation ---")
    
    # Clean up before testing
    User.objects.filter(username='EMP12345').delete()
    
    # Create a dummy image file using PIL
    from PIL import Image
    import io
    image = Image.new('RGB', (100, 100))
    img_io = io.BytesIO()
    image.save(img_io, format='JPEG')
    photo = SimpleUploadedFile("test_photo.jpg", img_io.getvalue(), content_type="image/jpeg")
    
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "employee_id": "EMP12345",
        "role": "Radiology Technician",
        "profile_picture": photo
    }

    response = client.post('/api/admincenter/users/', data, format='multipart')
    
    if response.status_code == 201:
        print("✅ User created successfully (201 Created).")
    else:
        print(f"❌ Failed to create user. Status: {response.status_code}")
        print(response.data)
        return False
        
    print("\n--- Verifying Database Records ---")
    user_exists = User.objects.filter(username='EMP12345').exists()
    
    if user_exists:
        user = User.objects.get(username='EMP12345')
        print("✅ User record was created successfully.")
        
        if hasattr(user, 'profile'):
            print("✅ UserProfile record linked successfully.")
            if user.profile.employee_id == 'EMP12345' and user.profile.role == 'Radiology Technician':
                print("✅ UserProfile data is correct.")
                if user.profile.profile_picture:
                    print("✅ UserProfile picture processed successfully.")
                else:
                    print("❌ UserProfile picture missing.")
                    return False
            else:
                print("❌ UserProfile data mismatch.")
                return False
        else:
            print("❌ UserProfile record was NOT created.")
            return False
            
    else:
        print("❌ User record was NOT created.")
        return False

    print("\nAll tests passed! Endpoint is ready for new_user_adding_slide.xml.")
    return True

if __name__ == '__main__':
    run_tests()
