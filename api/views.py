from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import *
from commute_share.models import *
from .permissions import *
from rest_framework.views import APIView


class DriverRegistrationView(generics.CreateAPIView):
    serializer_class = DriverSerializer
    queryset = DriverModel.objects.all()
    permission_classes = [IsUser]


class PassengerSignUpView(generics.CreateAPIView):
    queryset = PassengerModel.objects.all()
    serializer_class = PassengerSerializer
    permission_classes = [IsUser]


class CreateRideView(APIView):
    def post(self, request):
        serializer = RideSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class BookRideView(APIView):
    def post(self, request):
        serializer = PassengerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request):
        rides = RideModel.objects.all()
        serializer = RideSerializer(rides, many=True)
        return Response(serializer.data)


class DriverSignUpView(generics.CreateAPIView):
    queryset = DriverModel.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsUser]


class RideCreateView(generics.CreateAPIView):
    serializer_class = CreateRideSerializer
    permission_classes = [IsUser]


class RideView(generics.ListCreateAPIView):
    serializer_class = RideSerializer
    queryset = RideModel.objects.all()

    def perform_create(self, serializer):
        departure_location = self.request.data.get('departure_location')
        destination_location = self.request.data.get('destination_location')
        rides = CreateRide.objects.filter(destination_location=destination_location)

        for ride in rides:
            driver = ride.driver

            check_rider = CheckDrivers(driver=driver, car_color=driver.car.color,
                                       car_plate_number=driver.car.license_plate_number,
                                       phone_number=driver.user.phone_number,
                                       destination_location=destination_location, departure_time=ride.departure_time,
                                       available_seats=ride.available_seats)
            check_rider.save()

        serializer.save(departure_location=departure_location, destination_location=destination_location)


class CheckRiderView(generics.ListAPIView):
    serializer_class = CheckDriverSerializer
    queryset = CheckDrivers.objects.all()
