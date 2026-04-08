from rest_framework import viewsets, status, filters, pagination
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Machine, SystemLog, ComplianceReport, OnboardingSlide, SecuritySettings, VerificationCode
from .serializers import UserSerializer, MachineSerializer, SystemLogSerializer, ComplianceReportSerializer, OnboardingSlideSerializer, SecuritySettingsSerializer, ResetPasswordSerializer, VerificationCodeSerializer

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

from .utils import log_audit_activity

class UserManagementViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'profile__employee_id', 'profile__role']

    def perform_create(self, serializer):
        user = serializer.save()
        log_audit_activity('INFO', f"New user created: {user.username}", 'AdminControl', self.request.user if self.request.user.is_authenticated else None)

    def perform_update(self, serializer):
        user = serializer.save()
        log_audit_activity('INFO', f"User updated: {user.username}", 'AdminControl', self.request.user)

class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

class SystemLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SystemLog.objects.all().order_by('-timestamp')
    serializer_class = SystemLogSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['message', 'source', 'user__username', 'user__first_name', 'user__last_name']

class ComplianceReportViewSet(viewsets.ModelViewSet):
    queryset = ComplianceReport.objects.all().order_by('-generated_date')
    serializer_class = ComplianceReportSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(generated_by=self.request.user)
        else:
            serializer.save()

class OnboardingSlideViewSet(viewsets.ModelViewSet):
    queryset = OnboardingSlide.objects.all().order_by('slide_number')
    serializer_class = OnboardingSlideSerializer

class SecuritySettingsViewSet(viewsets.ModelViewSet):
    serializer_class = SecuritySettingsSerializer
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return SecuritySettings.objects.filter(user=self.request.user)
        return SecuritySettings.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SignUpView(CreateAPIView):
    """
    Dedicated endpoint for new user registration.
    Allows unauthenticated access.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print(f"DEBUG: Signup attempt for email: {request.data.get('email')}")
        response = super().post(request, *args, **kwargs)
        if response.status_code != 201:
            print(f"DEBUG: Signup failed with status {response.status_code}: {response.data}")
        return response

    def perform_create(self, serializer):
        user = serializer.save()
        log_audit_activity('INFO', f"Self-signup successful: {user.username}", 'Auth', user)

class SelectRoleView(APIView):
    def patch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        role = request.data.get('role')
        valid_roles = ["Radiologist", "CT Technician", "Hospital Admin"]
        if not role or role not in valid_roles:
            return Response({"error": f"Invalid role. Must be one of: {', '.join(valid_roles)}"}, status=status.HTTP_400_BAD_REQUEST)
        if hasattr(user, 'profile'):
            user.profile.role = role
            user.profile.save()
            return Response({"message": "Role successfully updated.", "role": role}, status=status.HTTP_200_OK)
        return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            log_audit_activity('INFO', f"Password reset for user: {user.username}", 'Auth', user)
            return Response({"message": "Password successfully reset."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserMeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
    def put(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            log_audit_activity('INFO', f"User updated their own profile: {request.user.username}", 'Profile', request.user)
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            log_audit_activity('INFO', f"User partially updated their own profile: {request.user.username}", 'Profile', request.user)
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class SendVerificationCodeView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=400)
        # Logic to send code would go here
        import random
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        VerificationCode.objects.create(email=email, code=code)
        print(f"DEBUG: Sent verification code {code} to {email}")
        return Response({"success": True, "message": "Verification code sent"})


class SendVerificationCodeView(APIView):
    """
    Generates and "sends" a 6-digit verification code to the user's email.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        import random
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        VerificationCode.objects.create(user=user, code=code)
        
        print(f"DEBUG: Verification code for {email} is {code}")
        
        # Actually send the email
        send_mail(
            'Password Reset Verification Code',
            f'Mawa, your 6-digit verification code is: {code}. Use this to reset your password.',
            'noreply@finalapp.com',
            [email],
            fail_silently=False,
        )
        
        return Response({
            "success": True,
            "message": f"Verification code sent to {email}",
            "code": code
        }, status=status.HTTP_200_OK)

class VerifyCodeView(APIView):
    """
    Verifies the 6-digit code entered by the user.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = VerificationCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data.get('code')
            
            try:
                user = User.objects.get(email=email)
                verification = VerificationCode.objects.filter(user=user, code=code, is_verified=False).order_by('-created_at').first()
                
                if verification:
                    verification.is_verified = True
                    verification.save()
                    return Response({"success": True, "message": "Verification successful!"}, status=status.HTTP_200_OK)
                else:
                    return Response({"success": False, "error": "Invalid or expired verification code"}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FinalResetPasswordView(APIView):
    """
    Sets a new password for a user after they have verified their code.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        code = request.data.get('code')
        new_password = request.data.get('new_password')
        
        if not all([email, code, new_password]):
            return Response({"error": "Email, code, and new_password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            # Find a verification code that has been marked as verified but not yet used
            verification = VerificationCode.objects.filter(user=user, code=code, is_verified=True).order_by('-created_at').first()
            
            if verification:
                user.set_password(new_password)
                user.save()
                # Mark verification as used by deleting it
                verification.delete()
                print(f"DEBUG: Password successfully reset for {email}")
                return Response({"success": True, "message": "Password reset successful!"}, status=status.HTTP_200_OK)
            else:
                return Response({"success": False, "error": "Invalid or unverified session"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
