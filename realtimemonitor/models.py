from django.db import models
from patients.models import Patient

class RealTimeDose(models.Model):
    patient = models.ForeignKey(Patient, related_name='realtime_doses', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    dose_rate = models.FloatField(help_text="Current dose rate in mGy/s")
    accumulated_dose = models.FloatField(help_text="Total accumulated dose during this session")
    is_active = models.BooleanField(default=True, help_text="Is the procedure still ongoing?")

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.patient.name} - {self.dose_rate} mGy/s at {self.timestamp.strftime('%H:%M:%S')}"
