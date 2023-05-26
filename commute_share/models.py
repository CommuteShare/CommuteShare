from django.utils import timezone

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class UserAdmin(AbstractUser):
    username = models.CharField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True)
    password = models.CharField(unique=True)


class User(models.Model):
    first_name = models.CharField(max_length=400, null=False, blank=False)
    last_name = models.CharField(max_length=400, null=False, blank=False)
    email = models.EmailField(blank=False, null=False)
    phone_number = PhoneNumberField()
    company = models.OneToOneField("CompanyModel", on_delete=models.PROTECT)


class CompanyModel(models.Model):
    name = models.CharField(max_length=400, null=False, blank=False)
    email = models.EmailField(blank=False, null=False)
    location = models.CharField(max_length=400, null=False, blank=False)


class PassengerModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    verification = models.OneToOneField("VerificationModel", on_delete=models.PROTECT)
    identity_verified = models.BooleanField()

    def book_ride(self, ride, driver, available_seats, departure_time, price):
        if available_seats <= 0:
            raise ValidationError("Invalid number of available seats.")

        if self.identity_verified is False:
            raise ValidationError("Passenger identity is not verified.")

        if ride.departure_location == ride.destination_location:
            raise ValidationError("Departure and destination locations cannot be the same.")

        if ride.departure_time <= departure_time:
            raise ValidationError("Invalid departure time.")

        book_ride = BookRideModel(
            ride=ride,
            passengers=self,
            driver=driver,
            available_seats=available_seats,
            departure_time=departure_time,
            price=price,
        )
        book_ride.available_seats -= 1
        notification = NotificationModel.objects.create(
            user=driver.user,
            passenger=self,
            is_read=False,
            created_at=timezone.now()
        )
        book_ride.save()
        return book_ride


class DriverModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    verification = models.OneToOneField("VerificationModel", on_delete=models.PROTECT)
    identity_verified = models.BooleanField()
    licence_number = models.CharField(max_length=10, null=False, blank=False)
    car = models.ForeignKey("CarModel", on_delete=models.PROTECT)

    def accept_ride(self, book_ride):
        if book_ride.driver != self:
            raise ValidationError("This ride does not belong to you.")

        book_ride.ride_status = 'CONFIRMED'
        book_ride.save()

        notification = NotificationModel.objects.get(user=self, passenger=book_ride.passengers)
        notification.is_read = True
        notification.save()

        return book_ride

    def get_unread_notifications(self):
        return NotificationModel.objects.filter(user=self, is_read=False)


class CustomerServiceModel(models.Model):
    RESPONSE_STATUS = [
        ('open', 'open'),
        ('in progress', 'progress'),
        ('closed', 'closed')

    ]
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    ride = models.ForeignKey("RideModel", on_delete=models.PROTECT)
    subject = models.CharField(null=False, blank=False)
    message = models.CharField(null=False, blank=False)
    response_status = models.CharField(null=False, blank=False, choices=RESPONSE_STATUS, default="closed")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class VerificationModel(models.Model):
    GENDER_STATUS = [
        ("MALE", "male"),
        ("FEMALE", "female")
    ]
    gender = models.CharField(null=False, blank=False, choices=GENDER_STATUS)
    id_card_front = models.ImageField(null=False, blank=False, upload_to="id-card-front/")
    id_card_back = models.ImageField(null=False, blank=False, upload_to="id-card-back/")
    photograph = models.ImageField(null=False, blank=False, upload_to="images1/")
    date_of_birth = models.DateField(null=False, blank=False, default='0000-00-0')


class CarModel(models.Model):
    license_plate_number = models.CharField(max_length=7, null=False, blank=False)
    identification_number = models.CharField(max_length=17, null=False, blank=False)
    color = models.CharField(null=False, blank=False)
    model = models.CharField()


class RideModel(models.Model):
    departure_location = models.CharField(null=False, blank=False)
    destination_location = models.CharField(null=False, blank=False)


class BookRideModel(models.Model):
    RIDE_STATUS = [
        ('CONFIRMED', 'confirmed'),
        ('PENDING', 'pending'),
        ('CANCELLED', 'cancelled')
    ]
    ride = models.ForeignKey(RideModel, on_delete=models.PROTECT)
    passengers = models.ForeignKey(PassengerModel, on_delete=models.PROTECT)
    driver = models.ForeignKey(DriverModel, on_delete=models.PROTECT)
    available_seats = models.IntegerField(null=False, blank=False)
    departure_time = models.TimeField(null=False, blank=False)
    ride_status = models.CharField(null=False, blank=False, choices=RIDE_STATUS, default='pending')
    price = models.DecimalField(max_digits=6, default=0, decimal_places=2)


class PaymentModel(models.Model):
    PAYMENT_STATUS = [
        ('SUCCESS', 'success'),
        ("PENDING", 'pending'),
        ("FAILED", 'failed')
    ]
    PAYMENT_METHOD = [
        ('BANK TRANSFER', 'transfer'),
        ("USSD", 'ussd'),
        ("CARD", 'card')
    ]
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    ride = models.ForeignKey(BookRideModel, on_delete=models.PROTECT)
    payment_status = models.CharField(null=False, blank=False, choices=PAYMENT_STATUS)
    payment_method = models.CharField(null=False, blank=False, choices=PAYMENT_METHOD)
    payment_description = models.CharField(null=False, blank=True)


class CreateRide(models.Model):
    departure_location = models.CharField(null=False, blank=False)
    destination_location = models.CharField(null=False, blank=False)
    departure_time = models.TimeField(null=False, blank=False)
    available_seats = models.IntegerField(null=False, blank=False)


class NotificationModel(models.Model):
    user = models.ForeignKey(DriverModel, on_delete=models.CASCADE)
    passenger = models.ForeignKey(PassengerModel, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
