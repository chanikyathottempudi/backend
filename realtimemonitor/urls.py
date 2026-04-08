from django.urls import path
from .views import RealTimeDoseViewSet

urlpatterns = [
    path('stream/', RealTimeDoseViewSet.as_view({'get': 'list', 'post': 'create'}), name='realtimedose-list'),
    path('stream/<int:pk>/', RealTimeDoseViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='realtimedose-detail'),
]
