from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Donations
from .serializers import *
from classifications.models import Classification

import json

from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse

from .permissions import *
from rest_framework.exceptions import PermissionDenied
from datetime import datetime
from django.shortcuts import get_object_or_404



class DonationView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsDonor]

    def get_serializer_class(self):
        return DonationSerializer

    def get_queryset(self):
        return Donations.objects.all()

    def perform_create(self, serializer):
        """ classification_id = self.request.data['classification']
        classification = Classification.objects.get(pk=classification_id) """

        classification_id = self.request.data["classification_id"]
        classification = get_object_or_404(Classification, id=classification_id)

        nowDate = datetime.now()
        dateFormat = f'{nowDate.year}-{nowDate.month}-{nowDate.day}'
        
        if self.request.data['expiration'] < dateFormat:
            raise PermissionDenied("Donating expired food is prohibited.")
        serializer.save(user=self.request.user, classification=classification)

        send_mail(
            subject="Aviso de cadastro de doação",
            message="Obrigado "
            + f"{self.request.user.responsible} "
            + "pela sua doação de "
            + f"{self.request.data['quantity']} "
            + "de "
            + f"{self.request.data['food']}"
            + ".",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[
                self.request.user.email,
            ],
            fail_silently=False,
        )


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