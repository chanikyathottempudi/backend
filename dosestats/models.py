from django.db import models
from patients.models import Patient

class ScanDose(models.Model):
    patient = models.ForeignKey(Patient, related_name='scan_doses', on_delete=models.CASCADE)
    scan_date = models.DateTimeField()
    study_description = models.CharField(max_length=200)
    total_dlp = models.FloatField(help_text="Total Dose Length Product")
    avg_risk = models.CharField(max_length=50, choices=[('Low', 'Low'), ('Moderate', 'Moderate'), ('High', 'High')])
    facility = models.CharField(max_length=200, default='Facility A', help_text="e.g., Facility A")

    def __str__(self):
        return f"{self.patient.name} - {self.scan_date.date()}"

class OrganDose(models.Model):
    scan = models.ForeignKey(ScanDose, related_name='organ_doses', on_delete=models.CASCADE)
    organ_name = models.CharField(max_length=100)
    dose_value = models.FloatField()

    def __str__(self):
        return f"{self.organ_name} dose for scan {self.scan.id}"

class DoseAnomaly(models.Model):
    patient = models.ForeignKey(Patient, related_name='anomalies', on_delete=models.CASCADE)
    anomaly_id = models.CharField(max_length=50, unique=True, help_text="#PX-000")
    area = models.CharField(max_length=100, help_text="e.g., Head, Chest")
    description = models.CharField(max_length=255)
    dlp_value = models.FloatField(help_text="Dose Length Product")
    status_level = models.CharField(max_length=50, choices=[('HIGH', 'HIGH'), ('CRITICAL', 'CRITICAL'), ('REVIEW', 'REVIEW')])
    detected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-detected_at']

    def __str__(self):
        return f"{self.anomaly_id} - {self.status_level}"

class ScanParameter(models.Model):
    patient = models.ForeignKey(Patient, related_name='scan_parameters', on_delete=models.SET_NULL, null=True, blank=True)
    kvp = models.FloatField(help_text="kVp value from Scan Parameters screen")
    ma = models.FloatField(help_text="mA value from Scan Parameters screen")
    pitch = models.FloatField(help_text="Pitch value from Scan Parameters screen")
    scan_length = models.FloatField(help_text="Scan Length (mm) from Scan Parameters screen")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Scan Parameters (kVp:{self.kvp}, mA:{self.ma}) at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
