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
    class Meta:
        model = CompanyModel
        fields = ['name', 'email', 'location']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class VerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationModel
        fields = ['gender', 'photograph', 'id_card_front', 'id_card_back']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class UserCreate(CreateSerializer):
    phone_number = PhoneNumberField()

    class Meta(CreateSerializer.Meta):
        fields = ['first_name', 'last_name', 'phone_number', 'username', 'email', 'password', 'is_driver']


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverModel
        fields = ['licence_number']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class CreateRideSerializer(serializers.ModelSerializer):
    driver_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CreateRide
        fields = ['driver_id', 'departure_location', 'destination_location', 'departure_time',
                  'available_seats', 'price']

    def create(self, validated_data):
        user = self.context['request'].user
        driver = DriverModel.objects.get(user=user)
        validated_data['driver'] = driver
        return super().create(validated_data)


class BookRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRideModel
        fields = ['destination_location', 'create_ride']


class CheckRide(serializers.Serializer):
    destination_location = serializers.CharField()


class BooksSerializer(serializers.ModelSerializer):
    create_ride = serializers.HyperlinkedRelatedField(
        queryset=CreateRide.objects.all(),
        view_name='ride_create-detail',
        lookup_field="pk"
    )

    class Meta:
        model = Books
        fields = ['create_ride']


class ChecksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checks
        fields = "__all__"


# class RideDetail(serializers.ModelSerializer):
#     class Meta:
