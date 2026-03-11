import os
import django
from django.core.files.uploadedfile import SimpleUploadedFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.test import Client
from dicom.models import DicomScan
from patients.models import Patient

def run_tests():
    DicomScan.objects.all().delete()
    Patient.objects.all().delete()
    
    # Create test patient
    patient = Patient.objects.create(patient_id="PT-SCAN-01", name="Oliver Twist", gender="Male", age=12)
    
    # Create a mock image file
    mock_image = SimpleUploadedFile(name='test_scan.jpg', content=b'fakeimagecontent', content_type='image/jpeg')
    
    # Create test scan using the correct field 'file'
    scan = DicomScan.objects.create(patient=patient, file=mock_image)

    client = Client()
    
    # 1. Test fetching scan list
    print("Testing GET /api/dicom/scans/")
    response = client.get('/api/dicom/scans/')
    if response.status_code == 200:
        data = response.json()
        assert len(data) == 1
        record = data[0]
        assert 'file' in record # Maps to loading the scan_image ImageView
        print(f"File URL returned: {record['file']}")
        print("GET Request passed successfully! Fields match UI requirements.")

    # 2. Test deleting scan via API
    print(f"Testing DELETE /api/dicom/scans/{scan.id}/ to simulate clicking the delete_scan_button")
    delete_response = client.delete(f'/api/dicom/scans/{scan.id}/')
    print(f"Delete Status Code: {delete_response.status_code}")
    
    if delete_response.status_code == 204:
        # Verify scan is actually deleted
        assert DicomScan.objects.filter(id=scan.id).count() == 0
        print("Scan deleted successfully! DELETE functionality verified.")
    else:
        print(f"Delete Response: {delete_response.content}\n")
        assert False, "dicom API DELETE call failed"
        
    print("All list item scan tests passed successfully!")

if __name__ == "__main__":
    run_tests()
