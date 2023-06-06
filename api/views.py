from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status

from rest_framework.response import Response

from .serializers import *
from commute_share.models import *


class DriverSignUpView(generics.CreateAPIView):
    queryset = DriverModel.objects.all()
    serializer_class = DriverSerializer


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


class BookRideView(ModelViewSet):
    serializer_class = BooksSerializer
    queryset = Books.objects.all()


class CheckRideView(ModelViewSet):
    queryset = CreateRide.objects.all()
    serializer_class = CheckRide

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        destination_location = serializer.validated_data.get('destination_location')

        check = CreateRide.objects.filter(destination_location=destination_location)
        print(check)

        for ride in check:
            Books.objects.create(
                driver=ride.driver,
                departure_location=ride.departure_location,
                destination_location=ride.destination_location,
                departure_time=ride.departure_time,
                available_seats=ride.available_seats,
                price=ride.price
            )

            books_serializer = BooksSerializer(data=ride, many=True)
            books_serializer.is_valid(raise_exception=True)
            books_serializer.save()

        return Response({"destination_location": destination_location}, status=status.HTTP_200_OK)


class ChecksView(ModelViewSet):
    queryset = Checks.objects.all()
    serializer_class = ChecksSerializer


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
