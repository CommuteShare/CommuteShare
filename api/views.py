from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status

from rest_framework.response import Response
from .permissions import IsDriver
from .serializers import *
from commute_share.models import *


class DriverSignUpView(generics.CreateAPIView):
    queryset = DriverModel.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsDriver]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class CarDetailView(ModelViewSet):
    queryset = CarModel.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsDriver]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class VerificationDetailView(ModelViewSet):
    queryset = VerificationModel.objects.all()
    serializer_class = VerificationSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class CompanyDetailView(ModelViewSet):
    queryset = CompanyModel.objects.all()
    serializer_class = CompanySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class CreateRideView(ModelViewSet):
    queryset = CreateRide.objects.all()
    lookup_field = "pk"
    serializer_class = CreateRideSerializer
    permission_classes = [IsDriver]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class BookRideView(ModelViewSet):
    serializer_class = BooksSerializer
    # lookup_field = "pk"
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

        for ride in check:
            Books.objects.create(create_ride=ride)
        return Response({"destination_location": destination_location}, status=status.HTTP_200_OK)


# class ChecksView(ModelViewSet):
#     queryset = Checks.objects.all()
#     serializer_class = ChecksSerializer


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
