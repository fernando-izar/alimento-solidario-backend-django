from django.shortcuts import render
from rest_framework import generics, status


class ReservationView(generics.ListCreateAPIView):
    ...


class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    ...


class ReservationUserView(generics.ListAPIView):
    ...
