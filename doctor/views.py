from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        identifier = request.data.get("username") # This can be Employee ID/Username or Email
        password = request.data.get("password")

        # MASTER ADMIN ENFORCEMENT
        MASTER_ADMIN_ID = "Admin999"
        MASTER_ADMIN_PASS = "Admin@Simats2026"
        MASTER_ADMIN_EMAIL = "admin@simats.com"
        
        if identifier == MASTER_ADMIN_ID or identifier == MASTER_ADMIN_EMAIL:
            if password != MASTER_ADMIN_PASS:
                 return Response(
                    {"success": False, "error": "Incorrect Admin Password"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        if not identifier or not password:
            return Response({"success": False, "error": "Username/Email and Password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Resolve User
        user_obj = None
        if "@" in identifier:
            user_obj = User.objects.filter(email=identifier).first()
        else:
            user_obj = User.objects.filter(username=identifier).first()

        if not user_obj:
            return Response({"success": False, "error": "Account not found with this ID/Email"}, status=status.HTTP_404_NOT_FOUND)

        # 2. Authenticate
        user = authenticate(username=user_obj.username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            
            # Get profile info if exists
            role = ""
            employee_id = ""
            if hasattr(user, 'profile'):
                role = user.profile.role
                employee_id = user.profile.employee_id

            return Response({
                "success": True,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": role,
                    "employee_id": employee_id
                }
            })
        
        return Response(
            {"success": False, "error": "Incorrect Password"},
            status=status.HTTP_401_UNAUTHORIZED
        )

import random
from admincenter.models import VerificationCode

class ForgotPasswordView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"success": False, "error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            # Generate a random 6-digit code
            code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            
            # Save to database (reusing admincenter model as planned)
            VerificationCode.objects.create(user=user, code=code)
            
            # In a real app, you would send an email/phone OTP here.
            print(f"DEBUG: Forgot Password OTP for {email} is {code}")
            
            return Response(
                {"success": True, "message": f"Verification code sent to {email}.", "code": code},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            # For security reasons, still return 200 but don't reveal code
            return Response(
                {"success": True, "message": f"If an account with {email} exists, a verification code has been sent."},
                status=status.HTTP_200_OK
            )





















