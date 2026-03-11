from django.db import models

class Patient(models.Model):
    patient_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=20)
    age = models.IntegerField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    room_number = models.CharField(max_length=50, null=True, blank=True)
    allergies = models.TextField(default="None")
    clinical_notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.patient_id})"

class DailyDose(models.Model):
    patient = models.ForeignKey(Patient, related_name='daily_doses', on_delete=models.CASCADE)
    date = models.DateField()
    dose_amount = models.FloatField()

    class Meta:
        unique_together = ('patient', 'date')
        ordering = ['date']

    def __str__(self):
        return f"Dose for {self.patient.name} on {self.date}"

class Alert(models.Model):
    patient = models.ForeignKey(Patient, related_name='alerts', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    alert_level = models.CharField(
        max_length=50, 
        choices=[('INFO', 'INFO'), ('WARNING', 'WARNING'), ('CRITICAL', 'CRITICAL')], 
        default='INFO'
    )
    dose_value_mSv = models.FloatField(null=True, blank=True, help_text="Measured dose related to the alert")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{'ACTIVE' if self.is_active else 'RESOLVED'}] {self.title} - {self.patient.name}"
