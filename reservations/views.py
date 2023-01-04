from django.shortcuts import render
from rest_framework import generics, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Reservations
from users.models import User
from .serializers import *
from django.shortcuts import get_object_or_404
from donations.models import Donations
from rest_framework.views import  Request
from reservations.permissions import *


class ReservationView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Reservations.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
       
       donation_id = self.request.data["donationId"]
       donation_obj = Donations.objects.get(pk = donation_id)
       serializer.save(user=self.request.user, donation =  donation_obj)

class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Reservations.objects.all()
    serializer_class = ReservationDetailSerializer

    lookup_url_kwarg = "pk"

class ReservationUserView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = ReservationSerializer
    queryset = Reservations.objects.all()

    """ def get_queryset(self): 
        user = self.request.user
        return user.id """


    