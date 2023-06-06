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
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import *
from commute_share.models import *
from .permissions import *
from rest_framework.views import APIView


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


class AcceptRideView(APIView):
    def post(self, request):
        driver = DriverModel.objects.get(user=request.user)
        book_ride_id = request.data.get('book_ride_id')

        try:
            book_ride = BookRideModel.objects.get(id=book_ride_id, driver=driver)
        except BookRideModel.DoesNotExist:
            return Response({'detail': 'Book ride not found.'}, status=status.HTTP_404_NOT_FOUND)

        book_ride.ride_status = 'CONFIRMED'
        book_ride.save()

        notification = NotificationModel.objects.get(user=driver.user, passenger=book_ride.passengers)
        notification.is_read = True
        notification.save()

        serializer = BookRideSerializer(book_ride)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StartRideView(APIView):
    def post(self, request, ):
        driver = DriverModel.objects.get(user=request.user)
        book_ride_id = request.data.get('book_ride_id')

        try:
            book_ride = BookRideModel.objects.get(id=book_ride_id, driver=driver)
        except BookRideModel.DoesNotExist:
            return Response({'detail': 'Book ride not found.'}, status=status.HTTP_404_NOT_FOUND)

        book_ride.ride_status = 'IN_PROGRESS'
        book_ride.save()

        serializer = BookRideSerializer(book_ride)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EndRideView(APIView):
    def post(self, request):
        driver = DriverModel.objects.get(user=request.user)
        book_ride_id = request.data.get('book_ride_id')

        try:
            book_ride = BookRideModel.objects.get(id=book_ride_id, driver=driver)
        except BookRideModel.DoesNotExist:
            return Response({'detail': 'Book ride not found.'}, status=status.HTTP_404_NOT_FOUND)

        book_ride.ride_status = 'COMPLETED'
        book_ride.save()

        serializer = BookRideSerializer(book_ride)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookRideView(ModelViewSet):
    serializer_class = BooksSerializer
    queryset = Books.objects.all()


class CheckRideView(ModelViewSet):
    queryset = CreateRide.objects.all()
    serializer_class = CheckRide

    def create(self, request, *args, **kwargs):
        data = request.data  # Get the request data

        # Ensure the data is in the expected dictionary format
        if not isinstance(data, dict):
            return Response({"non_field_errors": ["Invalid data. Expected a dictionary."]},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        destination_location = serializer.validated_data.get('destination_location')

        check = CreateRide.objects.filter(destination_location=destination_location)

        for ride in check:
            Books.objects.create(
                driver=ride.driver,
                departure_location=ride.departure_location,
                destination_location=ride.destination_location,
                departure_time=ride.departure_time,
                available_seats=ride.available_seats,
                price=ride.price
            )

            books_serializer = BooksSerializer(data=ride)
            books_serializer.is_valid(raise_exception=True)
            books_serializer.save()

        return Response({"destination_location": destination_location}, status=status.HTTP_200_OK)


class ChecksView(ModelViewSet):
    queryset = Checks.objects.all()
    serializer_class = ChecksSerializer
