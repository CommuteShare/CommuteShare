from rest_framework import serializers
from commute_share.models import *
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.permissions import IsAuthenticated
from djoser.serializers import UserCreateSerializer as CreateSerializer
from django.contrib.auth import get_user_model
import random


# User = get_user_model()


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['license_plate_number', 'identification_number', 'color', 'model']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyModel
        fields = ['user', 'name', 'email', 'location']


class VerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationModel
        fields = ['user', 'gender', 'photograph', 'id_card_front', 'id_card_back']

    def update(self, instance, validated_data):
        user_id = self.validated_data['user'].id
        instance.user.id = user_id
        instance.save()
        return instance


class UserCreate(CreateSerializer):
    phone_number = PhoneNumberField()

    class Meta(CreateSerializer.Meta):
        fields = ['first_name', 'last_name', 'phone_number', 'username', 'email', 'password', 'is_driver']


class DriverSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    verification = VerificationSerializer()
    car = CarSerializer()

    class Meta:
        model = DriverModel
        fields = ['user', 'company', 'verification', 'car', 'licence_number', 'identity_verified']

    def create(self, validated_data):
        company_data = validated_data.pop('company')
        user_data = company_data.pop('user')
        user_id = user_data.id

        company_data['user'] = user_id
        company_serializer = CompanySerializer(data=company_data)
        company_serializer.is_valid(raise_exception=True)
        company = company_serializer.save()

        verification_data = validated_data.pop('verification')
        user_data = verification_data.pop('user')
        user_id = user_data.id
        verification_data['user'] = user_id
        verification_serializer = VerificationSerializer(data=verification_data)
        verification_serializer.is_valid(raise_exception=True)
        verification = verification_serializer.save()

        car_data = validated_data.pop('car')
        car_serializer = CarSerializer(data=car_data)
        car_serializer.is_valid(raise_exception=True)
        car = car_serializer.save()

        driver = DriverModel.objects.create(user=self, company=company, verification=verification, car=car,
                                            **validated_data)
        return driver


class RideSerializer(serializers.Serializer):
    departure_location = serializers.CharField(max_length=1000)
    destination_location = serializers.CharField(max_length=1000)

    def create(self, validated_data):
        departure_location = validated_data.get('departure_location')
        destination_location = validated_data.get('destination_location')
        return {
            'departure_location': departure_location,
            'destination_location': destination_location
        }


class CreateRideSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = CreateRide
        fields = ['driver', 'departure_location', 'destination_location', 'departure_time', 'available_seats', 'price']

    def ride_price(self):
        self.price = 600
        return self.price * random.randint(1, 6)


class BookRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRideModel
        fields = ['driver']
