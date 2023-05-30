from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from commute_share.models import *
from .permissions import *
from rest_framework.views import APIView


class PassengerViewSet(ModelViewSet):
    queryset = PassengerModel.objects.all()
    serializer_class = PassengerSerializer
    permission_classes = [IsUser]

    def get_queryset(self):
        m_user = self.request.user
        if not m_user.is_authenticated:
            raise PermissionDenied("You must be authenticated to access this resource.")
        print(m_user.email)
        queryset = PassengerModel.objects.filter(user__first_name=m_user.first_name, user__last_name=m_user.last_name,
                                                 user__email=m_user.email)
        print(queryset)
        return queryset


# class DriverRegistrationView(generics.CreateAPIView):
#     serializer_class = DriverSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response({
#             'message': 'Driver registered successfully.',
#             'data': serializer.data
#         }, status=201, headers=headers)
#
#     def perform_create(self, serializer):
#         serializer.save()

# views.py


class DriverRegistrationView(generics.CreateAPIView):
    serializer_class = DriverSerializer
    queryset = DriverModel.objects.all()
    permission_classes = [IsUser]


# class DriverLoginView(generics.GenericAPIView):
#     serializer_class = DriverLoginSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         driver = serializer.validated_data
#         token, _ = Token.objects.get_or_create(user=driver)
#         return Response({'token': token.key})


class RideCreateView(generics.CreateAPIView):
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]


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



