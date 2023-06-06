from abc import ABC

from rest_framework import serializers
from commute_share.models import *
from phonenumber_field.serializerfields import PhoneNumberField
from djoser.serializers import UserCreateSerializer as CreateSerializer
import random


class CarSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CarModel
        fields = ['user_id', 'license_plate_number', 'identification_number', 'color', 'model']


class CompanySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CompanyModel
        fields = ['user_id', 'name', 'email', 'location']


class VerificationSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = VerificationModel
        fields = ['user_id', 'gender', 'photograph', 'id_card_front', 'id_card_back']


class UserCreate(CreateSerializer):
    phone_number = PhoneNumberField()

    class Meta(CreateSerializer.Meta):
        fields = ['first_name', 'last_name', 'phone_number', 'username', 'email', 'password', 'is_driver']


class DriverSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    company_id = serializers.IntegerField(read_only=True)
    verification_id = serializers.IntegerField(read_only=True)
    car_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = DriverModel
        fields = ['user_id', 'company_id', 'verification_id', 'car_id', 'licence_number']


class CreateRideSerializer(serializers.ModelSerializer):
    driver_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CreateRide
        fields = ['driver_id', 'departure_location', 'destination_location', 'departure_time',
                  'available_seats', 'price']


class BookRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRideModel
        fields = ['destination_location', 'create_ride']


class CheckRide(serializers.Serializer):
    destination_location = serializers.CharField()


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = "__all__"


class ChecksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checks
        fields = "__all__"
