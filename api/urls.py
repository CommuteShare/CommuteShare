from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register("passenger_view", PassengerViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path('api/driver/register/', DriverRegistrationView.as_view(), name='driver-register'),
    path('api/driver/login/', DriverLoginView.as_view(), name='driver-login'),
    path('api/ride/create/', RideCreateView.as_view(), name='ride-create'),
]
