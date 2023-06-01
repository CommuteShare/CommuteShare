from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status

from rest_framework.response import Response

from .serializers import *
from commute_share.models import *
from .permissions import *


# class PassengerCreateProfile(generics.CreateAPIView):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer
# permission_classes = [IsUser]


class DriverSignUpView(generics.CreateAPIView):
    queryset = DriverModel.objects.all()
    serializer_class = DriverSerializer
    # permission_classes = [IsAuthenticated]


class CarDetailView(ModelViewSet):
    queryset = CarModel.objects.all()
    serializer_class = CarSerializer


class VerificationDetailView(ModelViewSet):
    queryset = VerificationModel.objects.all()
    serializer_class = VerificationSerializer


class CompanyDetailView(ModelViewSet):
    queryset = CompanyModel.objects.all()
    serializer_class = CompanySerializer


class CreateRideView(generics.CreateAPIView):
    queryset = CreateRide.objects.all()
    serializer_class = CreateRideSerializer

    #
# class RideCreateView(generics.CreateAPIView):
#     serializer_class = CreateRideSerializer
#     permission_classes = [IsUser]
#
#
# class RideView(generics.ListCreateAPIView):
#     serializer_class = RideSerializer
#     queryset = RideModel.objects.all()
#
#     def perform_create(self, serializer):
#         departure_location = self.request.data.get('departure_location')
#         destination_location = self.request.data.get('destination_location')
#         rides = CreateRide.objects.filter(destination_location=destination_location)
#
#         for ride in rides:
#             driver = ride.driver
#
#             check_rider = CheckDrivers(driver=driver, car_color=driver.car.color,
#                                        car_plate_number=driver.car.license_plate_number,
#                                        phone_number=driver.user.phone_number,
#                                        destination_location=destination_location, departure_time=ride.departure_time,
#                                        available_seats=ride.available_seats)
#             check_rider.save()
#
#         serializer.save(departure_location=departure_location, destination_location=destination_location)
#
#
# class CheckRiderView(generics.ListAPIView):
#     serializer_class = CheckDriverSerializer
#     queryset = CheckDrivers.objects.all()
