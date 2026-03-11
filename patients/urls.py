from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, DailyDoseViewSet, AlertViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'daily-doses', DailyDoseViewSet)
router.register(r'alerts', AlertViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
