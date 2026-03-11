from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserManagementViewSet, 
    MachineViewSet, 
    SystemLogViewSet, 
    ComplianceReportViewSet, 
    OnboardingSlideViewSet,
    SecuritySettingsViewSet,
    SelectRoleView,
    SignUpView,
    ResetPasswordView,
    UserMeView,
    SendVerificationCodeView,
    VerifyCodeView
)

router = DefaultRouter()
router.register(r'users', UserManagementViewSet, basename='admin-users')
router.register(r'machines', MachineViewSet, basename='admin-machines')
router.register(r'logs', SystemLogViewSet, basename='admin-logs')
router.register(r'reports', ComplianceReportViewSet, basename='admin-reports')
router.register(r'onboarding-slides', OnboardingSlideViewSet, basename='admin-onboarding-slides')
router.register(r'security-settings', SecuritySettingsViewSet, basename='admin-security-settings')

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('select-role/', SelectRoleView.as_view(), name='select-role'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('me/', UserMeView.as_view(), name='user-me'),
    path('send-verification/', SendVerificationCodeView.as_view(), name='send-verification'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
]
