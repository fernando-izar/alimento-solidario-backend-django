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


class ReservationView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsCharity]

    queryset = Reservations.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
       donation_id = self.request.data["donation_id"]
       donation_obj = get_object_or_404(Donations, id=donation_id) 
       serializer.save(user=self.request.user, donation =  donation_obj)
       
class ReservationDetailView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsCharity]

    queryset = Reservations.objects.all()
    serializer_class = ReservationDetailSerializer
    lookup_url_kwarg = "pk" 
    
    """ def perform_create(self, serializer):
       donation_id = self.kwargs["pk"]
       donation_obj = get_object_or_404(Donations, pk=donation_id) 
       serializer.save(user=self.request.user, donation_id=donation_obj) 
 """
class ReservationCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsCharity]

    queryset = Reservations.objects.all()
    serializer_class = ReservationDetailSerializer

    

    def perform_create(self, serializer):
       donation_id = self.kwargs["pk"]
       donation_obj = get_object_or_404(Donations, id=donation_id) 
       serializer.save(user=self.request.user, donation_id =  donation_obj)

    """ def post (self, request: Request, pk) -> Response:
        donation_id = get_object_or_404(Donations, id=pk)
        serializer = ReservationDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(donation_id=donation_id, user = request.user)

        return Response(serializer.data)
 """
class ReservationUserView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ReservationSerializer
    queryset = Reservations.objects.all()



    