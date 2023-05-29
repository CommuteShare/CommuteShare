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


class PassengerViewSet(ModelViewSet):
    queryset = PassengerModel.objects.all()
    serializer_class = PassengerSerializer
    permission_classes = [IsUser]


class DriverViewSet(ModelViewSet):
    queryset = DriverModel.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsUser]


class RideCreateView(generics.CreateAPIView):
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]
