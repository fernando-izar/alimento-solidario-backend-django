from django.shortcuts import render
from rest_framework import generics, status


class ClassificationView(generics.ListCreateAPIView):
    ...


class ClassificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    ...


class ClassificationNameView(generics.ListAPIView):
    ...
