from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated


class UserView(generics.ListCreateAPIView):
    ...


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    ...


class UserProfileView(generics.ListAPIView):
    ...


class UserSoftDeleteView(generics.UpdateAPIView):
    ...
