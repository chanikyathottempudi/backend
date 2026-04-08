import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from patients.models import Patient

def populate_patients():
    patients_data = [
        {"name": "Aarav Sharma", "patient_id": "123456789", "gender": "Male", "allergies": "None"},
        {"name": "Ishani Gupta", "patient_id": "987654321", "gender": "Female", "allergies": "None"},
        {"name": "Vihaan Malhotra", "patient_id": "456789123", "gender": "Male", "allergies": "None"},
        {"name": "Diya Iyer", "patient_id": "789123456", "gender": "Female", "allergies": "None"},
        {"name": "Advait Joshi", "patient_id": "321654987", "gender": "Male", "allergies": "None"},
        {"name": "Rajesh Kumar", "patient_id": "P106", "gender": "Male", "allergies": "None"},
        {"name": "Priya Nair", "patient_id": "P107", "gender": "Female", "allergies": "None"},
        {"name": "Arjun Singh", "patient_id": "P108", "gender": "Male", "allergies": "None"},
        {"name": "Anjali Reddy", "patient_id": "P109", "gender": "Female", "allergies": "None"},
        {"name": "Vikram Patil", "patient_id": "P110", "gender": "Male", "allergies": "None"},
        {"name": "Sunita Deshmukh", "patient_id": "P111", "gender": "Female", "allergies": "None"},
        {"name": "Suresh Pillai", "patient_id": "P112", "gender": "Male", "allergies": "None"},
        {"name": "Kavita Hegde", "patient_id": "P113", "gender": "Female", "allergies": "None"}
    ]

    for data in patients_data:
        patient, created = Patient.objects.get_or_create(
            patient_id=data['patient_id'],
            defaults={
                'name': data['name'],
                'gender': data['gender'],
                'allergies': data['allergies']
            }
        )
        if created:
            print(f"Added patient: {data['name']}")
        else:
            print(f"Patient already exists: {data['name']}")

if __name__ == '__main__':
    populate_patients()
