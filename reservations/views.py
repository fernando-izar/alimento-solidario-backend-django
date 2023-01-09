from django.shortcuts import render
from rest_framework import generics, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Reservations
from users.models import User
from .serializers import *
from django.shortcuts import get_object_or_404
from donations.models import Donations
from rest_framework.views import  Request, APIView, Response, status
from reservations.permissions import *
from donations.serializers import DonationSerializer


class ReservationView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsCharity]

    queryset = Reservations.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
       donation_id = self.request.data["donation_id"]
       donation_obj = get_object_or_404(Donations, id=donation_id) 

       donation_obj.available = False

       obj = Donations.objects.get(pk=donation_id)
       obj.available = False
       obj.save()

       serializer.save(user=self.request.user, donation=donation_obj)
       
class ReservationDetailView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsCharity]

    queryset = Reservations.objects.all()
    serializer_class = ReservationDetailSerializer
    lookup_url_kwarg = "pk" 

class ReservationCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsCharity]

    queryset = Reservations.objects.all()
    serializer_class = ReservationDetailCreateSerializer

    lookup_field = "pk"

    def perform_create(self, serializer):
       donation_id = self.kwargs["pk"]
       donation_obj = get_object_or_404(Donations, id=donation_id) 

       donation_obj.available = False

       obj = Donations.objects.get(pk=donation_id)
       obj.available = False
       obj.save()

       serializer.save(user=self.request.user, donation =  donation_obj)

class ReservationUserView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ReservationSerializer
    queryset = Reservations.objects.all()



    