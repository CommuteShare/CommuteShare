from django.urls import path, include
from rest_framework import routers
from .views import *

urlpatterns = [
    path("driver_signup/", DriverSignUpView.as_view()),
    path("passenger_signup/", PassengerSignUpView.as_view()),
    path('ride/create/', RideCreateView.as_view(), name='ride-create'),
    path('ride/check/', RideView.as_view()),
    path('ride/all/' ,CheckRiderView.as_view()),
    # path('ride/check', ride_view)
]
