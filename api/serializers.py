from rest_framework import serializers
from commute_share.models import *
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.permissions import IsAuthenticated

from djoser.serializers import UserCreateSerializer as CreateSerializer


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['license_plate_number', 'identification_number', 'color']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyModel
        fields = ['name', 'email', 'location']


class UserSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'company']

    def create(self, validated_data):
        company_data = validated_data.pop('company')
        company = CompanyModel.objects.create(**company_data)
        validated_data['company'] = company
        user = User.objects.create(**validated_data)
        return user


class VerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationModel
        fields = ['gender', 'photograph', 'id_card_front', 'id_card_back', 'date_of_birth']


class PassengerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    verification = VerificationSerializer()

    class Meta:
        model = PassengerModel
        fields = ['user', 'verification', 'identity_verified']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        verification_data = validated_data.pop('verification')
        verification_serializer = VerificationSerializer(data=verification_data)
        verification_serializer.is_valid(raise_exception=True)
        verification = verification_serializer.save()

        passenger = PassengerModel.objects.create(user=user, verification=verification, **validated_data)
        return passenger


class UserCreate(CreateSerializer):
    phone_number = PhoneNumberField()

    class Meta(CreateSerializer.Meta):
        fields = ['first_name', 'last_name', 'phone_number', 'username', 'email', 'password']


class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    verify_driver = VerificationSerializer()
    car = CarSerializer()

    class Meta:
        model = DriverModel
        fields = ['user', 'car', 'verification', 'licence_number']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        verification_data = validated_data.pop('verification')
        verification_serializer = VerificationSerializer(data=verification_data)
        verification_serializer.is_valid(raise_exception=True)
        verification = verification_serializer.save()

        car_data = validated_data.pop('car')
        car_serializer = CarSerializer(data=car_data)
        car_serializer.is_valid(raise_exception=True)
        car = car_serializer.save()

        driver = DriverModel.objects.create(user=user, verification=verification, car=car, **validated_data)
        return driver


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideModel
        fields = ['id', 'driver', 'source', 'destination', 'departure_time']

    def create(self, validated_data):
        validated_data['driver'] = self.context['request'].user
        ride = RideModel.objects.create(**validated_data)
        return ride


class CreateRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateRide
        fields = ['departure_location', 'destination_location', 'departure_time', 'available_seats']
