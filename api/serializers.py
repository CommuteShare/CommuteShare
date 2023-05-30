from rest_framework import serializers
from commute_share.models import *
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.permissions import IsAuthenticated

from djoser.serializers import UserCreateSerializer as CreateSerializer


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


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['license_plate_number', 'identification_number', 'color', 'model']


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
        fields = ['gender', 'photograph', 'id_card_front', 'id_card_back']


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
    verification = VerificationSerializer()
    car = CarSerializer()

    class Meta:
        model = DriverModel
        fields = ['user', 'car', 'verification', 'licence_number', 'identity_verified']

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


# class DriverSerializer(serializers.ModelSerializer):
#     user = UserSerializer
#     verify_driver = VerificationSerializer
#     car = CarSerializer
#
#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         user_serializer = UserSerializer(data=user_data)
#         user_serializer.is_valid(raise_exception=True)
#         user = user_serializer.save()
#
#         verification_data = validated_data.pop('verification')
#         verification_serializer = VerificationSerializer(data=verification_data)
#         verification_serializer.is_valid(raise_exception=True)
#         verification = verification_serializer.save()
#
#         driver = DriverModel.objects.create(user=user, verification=verification, **validated_data)
#         return driver

# def validate_license_number(self, value):
#     existing_driver = DriverModel.objects.filter(license_number=value).first()
#     if existing_driver:
#         raise serializers.ValidationError('A driver with this license number already exists.')
#     return value
#
# class Meta:
#     model = DriverModel
#     fields = ('id', 'username', 'password', 'name', 'car_model', 'license_number')


class CheckDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckDrivers
        fields = "__all__"


class CreateRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateRide
        fields = ['driver', 'departure_location', 'destination_location', 'departure_time', 'available_seats']

# class BookRideSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BookRideModel
#         fields = ['driver']
