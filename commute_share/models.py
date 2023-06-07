from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
import random


# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True)
    is_driver = models.BooleanField(default=False)


class CompanyModel(models.Model):
    name = models.CharField(max_length=400, null=False, blank=False)
    email = models.EmailField(blank=False, null=False)
    location = models.CharField(max_length=400, null=False, blank=False)
    user = models.OneToOneField(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name}    "


class DriverModel(models.Model):
    licence_number = models.CharField(unique=True, max_length=10, null=False, blank=False)
    user = models.OneToOneField(User, on_delete=models.PROTECT)


class CustomerServiceModel(models.Model):
    RESPONSE_STATUS = [
        ('open', 'open'),
        ('in progress', 'progress'),
        ('closed', 'closed')

    ]
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    subject = models.CharField(null=False, blank=False, max_length=100)
    message = models.CharField(null=False, blank=False, max_length=100)
    response_status = models.CharField(null=False, blank=False, choices=RESPONSE_STATUS, default="closed",
                                       max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class VerificationModel(models.Model):
    GENDER_STATUS = [
        ("MALE", "male"),
        ("FEMALE", "female")
    ]

    gender = models.CharField(null=False, blank=False, choices=GENDER_STATUS, max_length=100)
    photograph = models.ImageField(null=False, blank=False, upload_to="images/")
    id_card_front = models.ImageField(null=False, blank=False, upload_to="id_card_front/")
    id_card_back = models.ImageField(null=False, blank=False, upload_to="id_card_back/")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Identity Verified"


class CarModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_plate_number = models.CharField(unique=True, max_length=7, null=False, blank=False)
    identification_number = models.CharField(unique=True, max_length=17, null=False, blank=False)
    color = models.CharField(null=False, blank=False, max_length=100)
    model = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.model} -- {self.color}"


class BookRideModel(models.Model):
    BOOK_RIDE_STATUS = [
        ('CONFIRMED', 'confirmed'),
        ('PENDING', 'pending'),
        ('IN PROGRESS', 'In progress'),
        ('CANCELED', 'canceled')
    ]
    destination_location = models.CharField(null=False, blank=False, max_length=1000)
    create_ride = models.OneToOneField('CreateRide', on_delete=models.CASCADE)


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
    payment_status = models.CharField(null=False, blank=False, choices=PAYMENT_STATUS, max_length=100)
    payment_method = models.CharField(null=False, blank=False, choices=PAYMENT_METHOD, max_length=100)
    payment_description = models.CharField(null=False, blank=True, max_length=100)


class CreateRide(models.Model):
    driver = models.ForeignKey(DriverModel, on_delete=models.CASCADE)
    departure_location = models.CharField(null=False, blank=False, max_length=1000)
    destination_location = models.CharField(null=False, blank=False, max_length=100)
    departure_time = models.TimeField(null=False, blank=False, max_length=100)
    available_seats = models.IntegerField(null=False, blank=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False, default=0)

    def check_ride(self, destination_location):
        return CreateRide.objects.filter(destination_location=destination_location)

    def __str__(self):
        return f'{self.driver.user.first_name}--{self.driver.user.last_name} '


class NotificationModel(models.Model):
    driver = models.ForeignKey(DriverModel, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Books(models.Model):
    create_ride = models.ForeignKey(CreateRide, on_delete=models.CASCADE)


class Checks(models.Model):
    books = models.OneToOneField(Books, on_delete=models.CASCADE)

#
# book_ride.available_seats -= 1
#         notification = NotificationModel.objects.create(
#             user=driver.user,
#             passenger=self,
#             is_read=False,
#             created_at=timezone.now()
#
#  book_ride = BookRideModel(
#             ride=ride,
#             passengers=self,
#             driver=driver,
#             available_seats=available_seats,
#             departure_time=departure_time,
#             price=price,
#         )
#         )
