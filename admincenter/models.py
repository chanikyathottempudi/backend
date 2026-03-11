from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Machine(models.Model):
    name = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('Online', 'Online'), ('Offline', 'Offline'), ('Maintenance', 'Maintenance')], default='Offline')
    last_calibration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.status})"

class SystemLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=20, choices=[('INFO', 'INFO'), ('WARNING', 'WARNING'), ('ERROR', 'ERROR'), ('CRITICAL', 'CRITICAL')])
    message = models.TextField()
    source = models.CharField(max_length=100, help_text="e.g., Auth, Database, Scanner")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"[{self.level}] {self.timestamp}: {self.message[:50]}"

class ComplianceReport(models.Model):
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    generated_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, default='New Report')
    description = models.TextField(null=True, blank=True)
    report_type = models.CharField(max_length=100, help_text="e.g., Monthly Dose Summary, HIPAA Audit")
    file = models.FileField(upload_to='compliance_reports/', null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.report_type}) - {self.generated_date.date()}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    employee_id = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    permissions_summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile ({self.role})"

class OnboardingSlide(models.Model):
    slide_number = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    description_1 = models.CharField(max_length=500, null=True, blank=True)
    description_2 = models.CharField(max_length=500, null=True, blank=True)
    description_3 = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"Slide {self.slide_number}: {self.title}"

class SecuritySettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='security_settings')
    biometric_login = models.BooleanField(default=False)
    data_encryption = models.BooleanField(default=True)
    automatic_logout = models.BooleanField(default=True)
    hipaa_compliance = models.BooleanField(default=True)

    def __str__(self):
        return f"Security Settings for {self.user.username}"

class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_codes')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Code {self.code} for {self.user.username} (Verified: {self.is_verified})"

@receiver(post_save, sender=User)
def create_user_security_settings(sender, instance, created, **kwargs):
    if created:
        SecuritySettings.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_security_settings(sender, instance, **kwargs):
    if hasattr(instance, 'security_settings'):
        instance.security_settings.save()

