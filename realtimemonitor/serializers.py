from rest_framework import serializers
from .models import RealTimeDose

class RealTimeDoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealTimeDose
        fields = ['id', 'patient', 'timestamp', 'dose_rate', 'accumulated_dose', 'is_active']
