from django.urls import path, include
from rest_framework import routers
from .views import *

urlpatterns = [
    path("driver_profile/", DriverSignUpView.as_view()),
    # path("passenger_create_profile/", PassengerCreateProfile.as_view()),

   path('ride/create/', CreateRideView.as_view(), name='ride-create'),
    # path('ride/check/', RideView.as_view()),
    # path('ride/all/' ,CheckRiderView.as_view()),
    # # path('ride/check', ride_view)
]

