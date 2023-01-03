from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Donations
from .serializers import *
from classifications.models import Classification


class DonationView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        return DonationSerializer

    def get_queryset(self):
        return Donations.objects.all()

    def perform_create(self, serializer):
        classification_id = self.request.data['classification']
        classification = Classification.objects.get(pk=classification_id)
        serializer.save(user=self.request.user, classification=classification)


class DonationDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = DonationDetailSerializer
    queryset = Donations.objects.all()

class DonationUserView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = DonationUserSerializer

    def get_queryset(self):
        user = self.request.user
        return [user]


class DonationExpandView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = DonationSerializer
    queryset = Donations.objects.all()


class DonationExpandDetailView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = DonationExpandDetailSerializer
    queryset = Donations.objects.all()
