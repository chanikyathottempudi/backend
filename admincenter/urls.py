from django.urls import path
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
    VerifyCodeView,
    FinalResetPasswordView
)

urlpatterns = [
    # Explicit ViewSet paths mapping standard actions
    path('users/', UserManagementViewSet.as_view({'get': 'list', 'post': 'create'}), name='admin-users-list'),
    path('users/<int:pk>/', UserManagementViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='admin-users-detail'),
    
    path('machines/', MachineViewSet.as_view({'get': 'list', 'post': 'create'}), name='admin-machines-list'),
    path('machines/<int:pk>/', MachineViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='admin-machines-detail'),

    path('logs/', SystemLogViewSet.as_view({'get': 'list'}), name='admin-logs-list'),
    path('logs/<int:pk>/', SystemLogViewSet.as_view({'get': 'retrieve'}), name='admin-logs-detail'),

    path('reports/', ComplianceReportViewSet.as_view({'get': 'list', 'post': 'create'}), name='admin-reports-list'),
    path('reports/<int:pk>/', ComplianceReportViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='admin-reports-detail'),

    path('onboarding-slides/', OnboardingSlideViewSet.as_view({'get': 'list', 'post': 'create'}), name='admin-onboarding-slides-list'),
    path('onboarding-slides/<int:pk>/', OnboardingSlideViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='admin-onboarding-slides-detail'),

    path('security-settings/', SecuritySettingsViewSet.as_view({'get': 'list', 'post': 'create'}), name='admin-security-settings-list'),
    path('security-settings/<int:pk>/', SecuritySettingsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='admin-security-settings-detail'),

    # Standard APIView pathways
    path('signup/', SignUpView.as_view(), name='signup'),
    path('select-role/', SelectRoleView.as_view(), name='select-role'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('me/', UserMeView.as_view(), name='user-me'),
    path('send-verification/', SendVerificationCodeView.as_view(), name='send-verification'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('final-reset-password/', FinalResetPasswordView.as_view(), name='final-reset-password'),
]
