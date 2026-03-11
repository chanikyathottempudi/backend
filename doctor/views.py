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

        if not identifier or not password:
            return Response({"success": False, "error": "Username/Email and Password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Determine if identifier is an email
        username = identifier
        if "@" in identifier:
            try:
                user_obj = User.objects.get(email=identifier)
                username = user_obj.username
            except User.DoesNotExist:
                pass # Fallback to original identifier

        # 2. Authenticate
        user = authenticate(username=username, password=password)

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
            {"success": False, "error": "Incorrect Employee ID/Email or Password"},
            status=status.HTTP_401_UNAUTHORIZED
        )

class ForgotPasswordView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user exists (Optional, depending on security preference to prevent email enumeration)
        # Even if the user doesn't exist, we usually return a success message for security reasons.
        user_exists = User.objects.filter(email=email).exists()
        
        # Here we would integrate with an email sending service (like Celery + SMTP)
        # For now, we simulate success since this is a backend for the app layout.
        
        return Response(
            {"message": f"If an account with {email} exists, a verification code has been sent."},
            status=status.HTTP_200_OK
        )





















