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
import pywhatkit
import pyautogui
import time


class ReservationView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsCharity]

    queryset = Reservations.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
       donation_id = self.request.data["donation_id"]
       donation_obj = get_object_or_404(Donations, id=donation_id) 
       serializer.save(user=self.request.user, donation =  donation_obj)
       
       contact_charity = self.request.user.contact
       pywhatkit.sendwhatmsg_instantly(phone_no=contact_charity, message="Sua reserva de " + f"{donation_obj.quantity} de " + f"{donation_obj.food} " +" foi registrada com sucesso, " + f"{self.request.user.name}! " + "Entre em contato com o doador " + f"{donation_obj.user.name}, " + "pelo telefone " + f"{donation_obj.user.contact}, " + "para combinar a retirada do produto.")
       time.sleep(3)
       pyautogui.click()
       time.sleep(3)


       contact_donor = donation_obj.user.contact
       pywhatkit.sendwhatmsg_instantly(phone_no=contact_donor, message="Sua doação de " + f"{donation_obj.quantity} de " + f"{donation_obj.food} " + "foi reservada, " + f"{donation_obj.user.name}! " + "Entre em contato com o donatário " + f"{self.request.user.name}, " +"através do telefone " + f"{self.request.user.contact}, " + "para combinar a entrega do produto.")
       time.sleep(3)
       pyautogui.click()
       time.sleep(3)
       
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

       serializer.save(user=self.request.user, donation =  donation_obj)

       contact_charity = self.request.user.contact
       pywhatkit.sendwhatmsg_instantly(phone_no=contact_charity, message="Sua reserva foi registrada com sucesso" + f"{self.request.user.name}! " + "Entre em contato com o doador " + f"{donation_obj.user.name} " + "pelo telefone " + f"{donation_obj.user.contact}" + "para combinar a retirada do produto.")
       time.sleep(10)
       pyautogui.click()
       time.sleep(3)


    #    contact_donor = donation_obj.user.contact
    #    pywhatkit.sendwhatmsg_instantly(phone_no=contact_donor, message="Sua doação foi reservada " + f"{donation_obj.user.name}! " + "Entre em contato com o donatário " + f"{self.request.user.name} " +"através do telefone" + f"{self.request.user.name} " + "para combinar a entrega do produto.")
    #    time.sleep(3)
    #    pyautogui.click()
    #    time.sleep(3)


class ReservationUserView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ReservationSerializer
    queryset = Reservations.objects.all()



    