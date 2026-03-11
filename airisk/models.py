from django.db import models
from patients.models import Patient

class PatientRiskAssessment(models.Model):
    patient = models.OneToOneField(Patient, related_name='risk_assessment', on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)
    
    # Overall Confidence
    confidence_level = models.CharField(max_length=50, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], default='Medium')
    
    # Key Metrics (as seen in the UI)
    high_risk_value = models.IntegerField(default=0)
    high_risk_desc = models.CharField(max_length=200, default='Processing...')
    
    pediatric_risk_value = models.IntegerField(default=0)
    pediatric_risk_desc = models.CharField(max_length=200, default='Processing...')
    
    protocol_deviations_value = models.IntegerField(default=0)
    protocol_deviations_desc = models.CharField(max_length=200, default='Processing...')

    def __str__(self):
        return f"Risk Assessment for {self.patient.name}"
