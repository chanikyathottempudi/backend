from django.db import models
from patients.models import Patient
import uuid

def dicom_upload_path(instance, filename):
    # Generates a path like media/dicom/patient_id/uuid.dcm
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    if instance.patient:
        return f"dicom/patient_{instance.patient.id}/{filename}"
    return f"dicom/unassigned/{filename}"

class DicomScan(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name='dicom_scans')
    file = models.FileField(upload_to=dicom_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='UPLOADED') # UPLOADED, PROCESSING, COMPLETED, FAILED

    def __str__(self):
        return f"Scan {self.id} for {self.patient.name if self.patient else 'Unknown'}"

class ScanRegistration(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='scan_registrations')
    requesting_physician = models.CharField(max_length=200)
    scan_type = models.CharField(max_length=100, default='CT')
    registered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='REGISTERED') # e.g., REGISTERED, COMPLETED

    def __str__(self):
        return f"{self.scan_type} Registration for {self.patient.name} by {self.requesting_physician}"
