from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Donations
from .serializers import DonationSerializer, DonationExpandSerializer, DonationFromUserSerializer
from .permissions import IsAccountOwner
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
    permission_classes = [IsAccountOwner]

    serializer_class = DonationExpandSerializer
    queryset = Donations.objects.all()

    lookup_url_kwarg = "pk"


class DonationUserView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]

    serializer_class = DonationFromUserSerializer
    queryset = Donations.objects.all()


class DonationExpandView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]

    serializer_class = DonationExpandSerializer
    queryset = Donations.objects.all()


class DonationExpandDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]

    serializer_class = DonationExpandSerializer
    queryset = Donations.objects.all()

    lookup_url_kwarg = "pk"
