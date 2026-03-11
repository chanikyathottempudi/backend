import os
import django
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.test import Client
from admincenter.models import OnboardingSlide

def run_test():
    print("Starting test_onboarding_slide.py...")
    
    # 1. Setup Data
    print("Setting up OnboardingSlide data...")
    # Clean up existing to ensure repeatable tests
    OnboardingSlide.objects.all().delete()
    
    slide = OnboardingSlide.objects.create(
        slide_number=2,
        title="Welcome to DoseStats",
        description_1="Empowering healthcare teams with real-time radiation dose tracking.",
        description_2="Enhancing patient safety through automated DRL alerts.",
        description_3="Optimizing clinical workflows with AI-driven insights."
    )
    print(f"Created slide: {slide}")
    
    # 2. Test the API Endpoint
    print("\nTesting GET /api/admincenter/onboarding-slides/...")
    client = Client()
    response = client.get('/api/admincenter/onboarding-slides/')
    
    # 3. Assertions
    print(f"Response Status Code: {response.status_code}")
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    response_data = response.json()
    print(f"Response Data:\n{json.dumps(response_data, indent=2)}")
    
    assert len(response_data) == 1, f"Expected 1 slide, got {len(response_data)}"
    
    returned_slide = response_data[0]
    assert returned_slide['slide_number'] == 2
    assert returned_slide['title'] == "Welcome to DoseStats"
    assert returned_slide['description_1'] == "Empowering healthcare teams with real-time radiation dose tracking."
    assert returned_slide['description_2'] == "Enhancing patient safety through automated DRL alerts."
    assert returned_slide['description_3'] == "Optimizing clinical workflows with AI-driven insights."
    
    print("\nAll tests passed successfully! The Onboarding Slide Backend is fully functional. 🚀")

if __name__ == '__main__':
    try:
        run_test()
    except AssertionError as e:
        print(f"\n❌ Test Failed: {e}")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
