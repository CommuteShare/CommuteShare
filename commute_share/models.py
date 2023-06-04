from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


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

    def book_ride(self, ride, driver, available_seats, departure_time, price):
        if available_seats <= 0:
            raise ValidationError("Invalid number of available seats.")

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
        notification.save()
        book_ride.save()
        return book_ride


class DriverModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    verification = models.OneToOneField("VerificationModel", on_delete=models.PROTECT)
    company = models.OneToOneField(CompanyModel, on_delete=models.PROTECT)
    car = models.ForeignKey("CarModel", on_delete=models.PROTECT)
    identity_verified = models.BooleanField()
    licence_number = models.CharField(unique=True, max_length=10, null=False, blank=False)

    def accept_ride(self, book_ride):
        if book_ride.driver != self:
            raise ValidationError("This ride does not belong to you.")

        book_ride.ride_status = 'CONFIRMED'
        book_ride.save()

        notification = NotificationModel.objects.get(user=self, passenger=book_ride.passengers)
        notification.is_read = True
        notification.save()

        return book_ride

    def start_ride(self, book_ride):
        if book_ride.driver != self:
            raise ValidationError("This ride does not belong to you.")

        book_ride.ride_status = 'IN_PROGRESS'
        book_ride.save()

        return book_ride

    def end_ride(self, book_ride):
        if book_ride.driver != self:
            raise ValidationError("This ride does not belong to you.")

        book_ride.ride_status = 'COMPLETED'
        book_ride.save()

        return book_ride


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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(null=False, blank=False, choices=GENDER_STATUS, max_length=1000)
    id_card_front = models.ImageField(null=False, blank=False, upload_to="id-card-front/")
    id_card_back = models.ImageField(null=False, blank=False, upload_to="id-card-back/")
    photograph = models.ImageField(null=False, blank=False, upload_to="images1/")
    date_of_birth = models.DateField(null=False, blank=False, default='0000-00-0')


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
        return f'{self.driver.user.first_name}--{self.driver.user.last_name}'

    def check_ride(self, destination_location):
        return CreateRide.objects.filter(destination_location=destination_location)

    def __str__(self):
        return f'{self.driver.user.first_name}--{self.driver.user.last_name}'


class NotificationModel(models.Model):
    driver = models.ForeignKey(DriverModel, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
