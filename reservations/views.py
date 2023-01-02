from django.shortcuts import render
from rest_framework import generics, status
from rest_framework_simplejwt import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Reservations
from users.models import User
from .serializers import ReservationsSerializer
from django.shortcuts import get_object_or_404
from donations.models import Donations


class ReservationView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Reservations.objects.all()
    serializer_class = ReservationsSerializer

    def perform_create(self, serializer):
        donation_obj= get_object_or_404(User, pk=self.kwargs["pk"])
        serializer.save(donation = donation_obj)

    ...


class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Reservations.objects.all()
    serializer_class = ReservationsSerializer

    lookup_url_kwarg = "pk"
    
    ...


class ReservationUserView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Reservations.objects.all()
    serializer_class = ReservationsSerializer
    ...
