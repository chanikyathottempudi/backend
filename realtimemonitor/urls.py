from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RealTimeDoseViewSet

router = DefaultRouter()
router.register(r'stream', RealTimeDoseViewSet, basename='realtimedose')

urlpatterns = [
    path('', include(router.urls)),
]
