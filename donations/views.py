from django.shortcuts import render
from rest_framework import generics, status


class DonationView(generics.ListCreateAPIView):
    ...


class DonationDetailView(generics.RetrieveUpdateDestroyAPIView):
    ...


class DonationUserView(generics.ListAPIView):
    ...


class DonationExpandView(generics.ListCreateAPIView):
    ...


class DonationExpandDetailView(generics.RetrieveUpdateDestroyAPIView):
    ...
