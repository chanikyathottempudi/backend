from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from .models import Machine, SystemLog, ComplianceReport, UserProfile, OnboardingSlide, SecuritySettings

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True, required=False)
    employee_id = serializers.CharField(write_only=True, required=False)
    role = serializers.CharField(write_only=True)
    profile_picture = serializers.ImageField(write_only=True, required=False)
    phone_number = serializers.CharField(write_only=True, required=False)
    permissions_summary = serializers.CharField(write_only=True, required=False)
    
    # Read-only fields to surface profile info
    employee_id_display = serializers.CharField(source='profile.employee_id', read_only=True)
    role_display = serializers.CharField(source='profile.role', read_only=True)
    profile_picture_url = serializers.ImageField(source='profile.profile_picture', read_only=True)
    phone_number_display = serializers.CharField(source='profile.phone_number', read_only=True)
    permissions_summary_display = serializers.CharField(source='profile.permissions_summary', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'is_staff', 'is_active', 'date_joined', 
                  'employee_id', 'role', 'profile_picture', 'phone_number', 'permissions_summary', 'full_name',
                  'employee_id_display', 'role_display', 'profile_picture_url', 'phone_number_display', 'permissions_summary_display']
        extra_kwargs = {
            'username': {'required': False},
            'password': {'write_only': True, 'required': False} # Password might be optional for updates
        }

    def validate(self, data):
        email = data.get('email')
        employee_id = data.get('employee_id')
        
        # If no employee_id provided, it will fallback to email in create()
        # So we should check if the email-based username/employee_id would collide
        check_id = employee_id if employee_id else (email[:50] if email else None)
        
        if self.instance: # Update
            if email and User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
                raise serializers.ValidationError({"email": "A user with this email already exists."})
            if check_id and User.objects.exclude(pk=self.instance.pk).filter(username=check_id).exists():
                raise serializers.ValidationError({"employee_id": "A user with this Employee ID/Email already exists."})
            if check_id and UserProfile.objects.exclude(user=self.instance).filter(employee_id=check_id).exists():
                raise serializers.ValidationError({"employee_id": "This Employee ID is already in use by another profile."})
        else: # Create
            if email and User.objects.filter(email=email).exists():
                raise serializers.ValidationError({"email": "A user with this email already exists."})
            if check_id and User.objects.filter(username=check_id).exists():
                raise serializers.ValidationError({"employee_id": "A user with this Employee ID already exists."})
            if check_id and UserProfile.objects.filter(employee_id=check_id).exists():
                raise serializers.ValidationError({"employee_id": "This Employee ID is already in use."})
                
        return data

    @transaction.atomic
    def create(self, validated_data):
        full_name = validated_data.pop('full_name', None)
        employee_id = validated_data.pop('employee_id', None)
        role = validated_data.pop('role')
        profile_picture = validated_data.pop('profile_picture', None)
        phone_number = validated_data.pop('phone_number', None)
        permissions_summary = validated_data.pop('permissions_summary', None)
        password = validated_data.pop('password', None)
        email = validated_data.get('email')
        
        if full_name:
            names = full_name.split(' ', 1)
            validated_data['first_name'] = names[0]
            if len(names) > 1:
                validated_data['last_name'] = names[1]
        
        if not employee_id and email:
            # Fallback to using email as employee_id/username if not provided
            employee_id = email[:50] # Truncate if necessary to fit in UserProfile.employee_id
        
        if not employee_id:
             raise serializers.ValidationError({"employee_id": "Employee ID or Email is required."})

        # We'll use employee_id as the username if one wasn't provided
        if 'username' not in validated_data:
            validated_data['username'] = employee_id[:150] # Ensure it fits in User.username
            
        # Use create_user to ensure password hashing
        if not password:
            password = employee_id # Default password
            
        user = User.objects.create_user(password=password, **validated_data)
        
        # Create the associated profile
        UserProfile.objects.create(
            user=user,
            employee_id=employee_id,
            role=role,
            profile_picture=profile_picture,
            phone_number=phone_number,
            permissions_summary=permissions_summary
        )
        
        return user

    @transaction.atomic
    def update(self, instance, validated_data):
        # Extract profile data
        employee_id = validated_data.pop('employee_id', None)
        role = validated_data.pop('role', None)
        profile_picture = validated_data.pop('profile_picture', None)
        phone_number = validated_data.pop('phone_number', None)
        permissions_summary = validated_data.pop('permissions_summary', None)

        # Update User instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update or create Profile instance
        profile, created = UserProfile.objects.get_or_create(user=instance)
        if employee_id is not None:
            profile.employee_id = employee_id
        if role is not None:
            profile.role = role
        if profile_picture is not None:
            profile.profile_picture = profile_picture
        if phone_number is not None:
            profile.phone_number = phone_number
        if permissions_summary is not None:
            profile.permissions_summary = permissions_summary
        profile.save()

        return instance

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'

class SystemLogSerializer(serializers.ModelSerializer):
    user_display = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = SystemLog
        fields = ['id', 'timestamp', 'level', 'message', 'source', 'user', 'user_display']

class ComplianceReportSerializer(serializers.ModelSerializer):
    generated_by_username = serializers.CharField(source='generated_by.username', read_only=True)

    class Meta:
        model = ComplianceReport
        fields = ['id', 'generated_by', 'generated_by_username', 'generated_date', 'title', 'description', 'report_type', 'file']

class OnboardingSlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingSlide
        fields = '__all__'

class SecuritySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecuritySettings
        fields = ['id', 'user', 'biometric_login', 'data_encryption', 'automatic_logout', 'hipaa_compliance']
        read_only_fields = ['user']

class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)
    repeat_password = serializers.CharField(write_only=True, required=True, min_length=8)

    def validate(self, data):
        if data['new_password'] != data['repeat_password']:
            raise serializers.ValidationError({"repeat_password": "Passwords must match."})
        return data

class VerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(max_length=6, min_length=6, required=False)
