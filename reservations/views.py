from django.shortcuts import render
from rest_framework import generics, status
from rest_framework_simplejwt import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Reservations
from users.models import User
from .serializers import ReservationsSerializer


class ReservationView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Reservations.objects.all()
    serializer_class = ReservationsSerializer
    ...


class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Reservations.objects.all()
    serializer_class = ReservationsSerializer
    
    ...


class ReservationUserView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    ...
