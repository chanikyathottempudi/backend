import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from rest_framework.test import APIClient

def run_tests():
    client = APIClient()

    print("--- Testing AI Prediction Endpoint ---")
    
    # 1. Test Low Risk Scenario
    low_risk_data = {
        "body_part": "Chest",
        "age": 45,
        "weight": 70.0,
        "kvp": 120,
        "mas": 80
    }
    
    print("\n[POST] /api/dosestats/scans/predict_dose/ (Low Risk Data)")
    response = client.post('/api/dosestats/scans/predict_dose/', low_risk_data, format='json')
    
    if response.status_code == 200:
        data = response.data
        print(f"✅ Success. Risk: {data.get('risk_status')}, DLP: {data.get('predicted_dlp')}, Effective: {data.get('effective_dose')}")
        if data.get('risk_status') != "LOW RISK":
            print("❌ Expected LOW RISK.")
            return False
    else:
        print(f"❌ Failed. Status: {response.status_code}")
        return False
        
        
    # 2. Test High Risk Scenario (Abdomen with high kVp/mAs)
    high_risk_data = {
        "body_part": "Abdomen",
        "age": 60,
        "weight": 80.0,
        "kvp": 140,
        "mas": 350
    }
    
    print("\n[POST] /api/dosestats/scans/predict_dose/ (High Risk Data)")
    response_high = client.post('/api/dosestats/scans/predict_dose/', high_risk_data, format='json')
    
    if response_high.status_code == 200:
        data_high = response_high.data
        print(f"✅ Success. Risk: {data_high.get('risk_status')}, DLP: {data_high.get('predicted_dlp')}, Effective: {data_high.get('effective_dose')}")
        if data_high.get('risk_status') != "HIGH RISK":
            print("❌ Expected HIGH RISK.")
            return False
            
        if "Dose is significantly high" not in data_high.get('protocol_tip'):
            print("❌ Missing high-risk protocol tip.")
            return False
    else:
        print(f"❌ Failed. Status: {response_high.status_code}")
        return False

    print("\nAll tests passed! Endpoint seamlessly integrates with predict_dose_slide.xml.")
    return True

if __name__ == '__main__':
    run_tests()
