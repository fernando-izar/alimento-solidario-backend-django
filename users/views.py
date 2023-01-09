from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdm, IsOwnerOrAdm
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import pywhatkit
import datetime
import pyautogui
import time
import keyboard as k


class UserView(generics.ListCreateAPIView):

    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            self.authentication_classes = [JWTAuthentication]
            self.permission_classes = [IsAuthenticated, IsAdm]
        return super().dispatch(request, *args, **kwargs)

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):

        current_time = datetime.datetime.now()
        # pywhatkit.sendwhatmsg(phone_no=self.request.POST["contact"], message="Bem vindo ao Alimento Solidário! Seu cadatro foi realizado com sucesso!")
        # pywhatkit.sendwhatmsg(phone_no="+5517981026092", message="Bem vindo ao Alimento Solidário! Seu cadatro foi realizado com sucesso!", time_hour=current_time.hour, time_min=current_time.minute)
        # pywhatkit.sendwhatmsg(phone_no="+5517981026092", message="Bem vindo ao Alimento Solidário! Seu cadatro foi realizado com sucesso!", time_hour=17, time_min=15)
        pywhatkit.sendwhatmsg_instantly(phone_no="+5517981026092", message="Bem vindo ao Alimento Solidário! Seu cadastro foi realizado com sucesso!")
        time.sleep(2)
        pyautogui.click()
        time.sleep(1)
        pyautogui.press('enter')



        return super().perform_create(serializer)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrAdm]

    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if not user.isActive:
            return Response({"error": "User already deleted"}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

      
class UserProfileView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class UserSoftDeleteView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrAdm]
    lookup_field = "pk"

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if not user.isActive:
            return Response({"error": "User already deleted"}, status=status.HTTP_400_BAD_REQUEST)
        user.isActive = False
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

