from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.SimpleRouter()
router.register("cars", CarDetailView, basename="cars")
router.register("companies", CompanyDetailView, basename="companies")
router.register("verifications", VerificationDetailView, basename="verifications")
router.register('book_rides', BookRideView, basename='book-ride')
router.register('destination', CheckRideView)
router.register('checks', ChecksView)
urlpatterns = [
    path('', include(router.urls)),
    path("driver_profile/", DriverSignUpView.as_view()),
    path('ride/create/', CreateRideView.as_view(), name='ride-create'),
]
