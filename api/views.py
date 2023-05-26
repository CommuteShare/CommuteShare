from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from commute_share.models import *
from .permissions import *


class PassengerViewSet(ModelViewSet):
    queryset = PassengerModel.objects.all()
    serializer_class = PassengerSerializer
    permission_classes = [IsUser]

    def get_queryset(self):
        m_user = self.request.user
        if not m_user.is_authenticated:
            raise PermissionDenied("You must be authenticated to access this resource.")
        print(m_user.email)
        queryset = PassengerModel.objects.filter(user__first_name=m_user.first_name, user__last_name=m_user.last_name,
                                                 user__email=m_user.email)
        print(queryset)
        return queryset
