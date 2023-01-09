from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Donations
from .serializers import *
from classifications.models import Classification
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

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

    serializer_class = DonationDetailSerializer
    queryset = Donations.objects.all()

    @extend_schema(
        operation_id="create_donation",
        parameters=[
            DonationSerializer,
        ],
        request=DonationSerializer,
        responses={201: DonationSerializer},
        description="Rota para criação de doações",
        summary="Criação de doações",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @extend_schema(
        operation_id="list_donations",
        parameters=[
            DonationSerializer,
        ],
        responses={201: DonationSerializer},
        description="Rota para listagem de doações",
        summary="Listagem de doações",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_class(self):
        return DonationSerializer

    def get_queryset(self):
        return Donations.objects.all()

    def perform_create(self, serializer):

        classification_id = self.request.data["classification_id"]
        classification = get_object_or_404(Classification, id=classification_id)

        nowDate = datetime.now()
        dateFormat = f"{nowDate.year}-{nowDate.month}-{nowDate.day}"

        if self.request.data["expiration"] < dateFormat:
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

    @extend_schema(
        operation_id="get_donation_by_id",
        parameters=[
            DonationDetailSerializer,
        ],
        request=DonationDetailSerializer,
        responses={201: DonationDetailSerializer},
        description="Rota para mostrar a doação pelo ID",
        summary="Mostra a doação",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        operation_id="update_donation_by_id",
        parameters=[
            DonationDetailSerializer,
        ],
        request=DonationDetailSerializer,
        responses={201: DonationDetailSerializer},
        description="Rota para atualizar a doação pelo ID",
        summary="Atualiza a doação",
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        exclude=True,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        operation_id="delete_donation_by_id",
        description="Rota para excluir a doação pelo ID",
        summary="Exclui a doação",
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class DonationUserView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = DonationUserSerializer

    queryset = Donations.objects.all()

    @extend_schema(
        operation_id="get_donation_with_donor",
        parameters=[
            DonationUserSerializer,
        ],
        request=DonationUserSerializer,
        responses={201: DonationUserSerializer},
        description="Rota para mostrar a doação com o doador",
        summary="Mostra a doação e o doador",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return [user]
