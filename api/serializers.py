from abc import ABC

from rest_framework import serializers
from commute_share.models import *
from phonenumber_field.serializerfields import PhoneNumberField
from djoser.serializers import UserCreateSerializer as CreateSerializer
import random


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['user', 'license_plate_number', 'identification_number', 'color', 'model']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyModel
        fields = ['user', 'name', 'email', 'location']


class VerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationModel
        fields = ['user', 'gender', 'photograph', 'id_card_front', 'id_card_back']


class UserCreate(CreateSerializer):
    phone_number = PhoneNumberField()

    class Meta(CreateSerializer.Meta):
        fields = ['first_name', 'last_name', 'phone_number', 'username', 'email', 'password', 'is_driver']


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverModel
        fields = ['user', 'company', 'verification', 'car', 'licence_number', 'identity_verified']


class CreateRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateRide
        fields = ['driver', 'departure_location', 'destination_location', 'departure_time',
                  'available_seats', 'price']


class BookRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRideModel
        fields = ['destination_location', 'create_ride']


class CheckRide(serializers.Serializer):
    destination_location = serializers.CharField()


class BooksSerializer(serializers.ModelSerializer):
    create_ride = CreateRide

    class Meta:
        model = Books
        fields = "__all__"


class ChecksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checks
        fields = "__all__"

