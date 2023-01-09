from django.shortcuts import render
from rest_framework import generics, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdm, IsOwnerOrAdm
from .serializers import ClassificationSerializer
from .models import Classification
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


class ClassificationView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdm]

    queryset = Classification.objects.all()
    serializer_class = ClassificationSerializer


class ClassificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdm]

    queryset = Classification.objects.all()
    serializer_class = ClassificationSerializer


class ClassificationNameView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Classification.objects.all()
    serializer_class = ClassificationSerializer
    lookup_field = "name"
