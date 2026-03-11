from rest_framework import viewsets, status, filters, pagination
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Machine, SystemLog, ComplianceReport, OnboardingSlide, SecuritySettings, VerificationCode
from .serializers import UserSerializer, MachineSerializer, SystemLogSerializer, ComplianceReportSerializer, OnboardingSlideSerializer, SecuritySettingsSerializer, ResetPasswordSerializer, VerificationCodeSerializer

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserManagementViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'profile__employee_id', 'profile__role']

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
        # Automatically set the generated_by field to the logged-in user if request.user is available
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
        # Only return the settings for the currently authenticated user
        if self.request.user.is_authenticated:
            return SecuritySettings.objects.filter(user=self.request.user)
        return SecuritySettings.objects.none()

    def perform_create(self, serializer):
        # Automatically assign the logged-in user to the settings
        serializer.save(user=self.request.user)


class SignUpView(CreateAPIView):
    """
    Dedicated endpoint for new user registration.
    Allows unauthenticated access.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class SelectRoleView(APIView):
    """
    Endpoint for users to select their role during onboarding.
    Accepts PATCH requests with a 'role' field.
    """
    def patch(self, request, *args, **kwargs):
        user = request.user
        
        if not user.is_authenticated:
            return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
            
        role = request.data.get('role')
        valid_roles = ["Radiologist", "CT Technician", "Hospital Admin"]
        
        if not role or role not in valid_roles:
            return Response(
                {"error": f"Invalid role. Must be one of: {', '.join(valid_roles)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Ensure the user has a profile, and update the role
        if hasattr(user, 'profile'):
            user.profile.role = role
            user.profile.save()
            return Response({"message": "Role successfully updated.", "role": role}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordView(APIView):
    """
    Endpoint for newly authenticated users to reset their password.
    Requires authentication. Accepts 'new_password' and 'repeat_password'.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Password successfully reset."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserMeView(APIView):
    """
    Endpoint for the currently authenticated user to retrieve their own profile details.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

import random

class SendVerificationCodeView(APIView):
    """
    Generates and "sends" a 6-digit verification code to the user's email.
    For this demo, we just log it and return it in the response (not for production!).
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
        
        # Generate a random 6-digit code
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        # Save to database
        VerificationCode.objects.create(user=user, code=code)
        
        # In a real app, you would send an email here.
        print(f"DEBUG: Verification code for {email} is {code}")
        
        return Response({
            "message": f"Verification code sent to {email}",
            "code": code # Returning code for testing purposes
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
            
            if not code:
                return Response({"error": "Code is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                user = User.objects.get(email=email)
                # Check the latest code for this user
                verification = VerificationCode.objects.filter(user=user, code=code, is_verified=False).order_by('-created_at').first()
                
                if verification:
                    verification.is_verified = True
                    verification.save()
                    return Response({"message": "Verification successful!"}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid or expired verification code"}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
