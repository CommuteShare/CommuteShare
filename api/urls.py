from django.urls import path, include
from rest_framework import routers
from .views import *

router1 = routers.DefaultRouter()
router2= routers.DefaultRouter()
router1.register("passenger_view", PassengerViewSet)
router2.register("driver_view",DriverViewSet)
urlpatterns = [
    path("", include(router1.urls)),
    path("", include(router2.urls)),
    path('api/ride/create/', RideCreateView.as_view(), name='ride-create'),
]
