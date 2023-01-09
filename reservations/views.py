from django.shortcuts import render
from rest_framework import generics, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Reservations
from users.models import User
from .serializers import *
from django.shortcuts import get_object_or_404
from donations.models import Donations
from rest_framework.views import Request, APIView, Response, status
from reservations.permissions import *
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from donations.serializers import DonationSerializer

from django.core.mail import send_mail
from django.conf import settings


class ReservationView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsCharity]

    queryset = Reservations.objects.all()
    serializer_class = ReservationSerializer

    @extend_schema(
        operation_id="create_reservation_by_body_id",
        parameters=[
            ReservationSerializer,
        ],
        request=ReservationSerializer,
        responses={201: ReservationSerializer},
        description="Rota para criação de reservas enviando id pelo body",
        summary="Criação de reservas",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @extend_schema(
        operation_id="list_reservations_by_donor_charity",
        parameters=[
            ReservationSerializer,
        ],
        responses={201: ReservationSerializer},
        description="Rota para listagem de reservas com dados do doador e donatário",
        summary="Listagem de reservas",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):

        donation_id = self.request.data["donation_id"]
        donation_obj = get_object_or_404(Donations, id=donation_id)

        donation_obj.available = False

        obj = Donations.objects.get(pk=donation_id)
        obj.available = False
        obj.save()

        serializer.save(user=self.request.user, donation=donation_obj)

        send_mail(
            subject="Aviso de reserva de doação",
            message="Obrigado "
            + f"{self.request.user.responsible} "
            + "pela sua reserva de "
            + f"{donation_obj.quantity} "
            + "de "
            + f"{donation_obj.food}"
            + "! O responsável por essa doação é a empresa "
            + f"{donation_obj.user.name}"
            + " e você poderá entrar em contato com o "
            + f"{donation_obj.user.responsible} "
            + "no número "
            + f"{donation_obj.user.contact} "
            + "para proceder com a sua retirada da mercadoria reservada. O endereço é: "
            + f"{donation_obj.user.address.address}"
            + ", "
            + f"{donation_obj.user.address.complement}"
            + " na cidade de "
            + f"{donation_obj.user.address.city}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[
                self.request.user.email,
            ],
            fail_silently=False,
        )

        send_mail(
            subject="Aviso de reserva de doação",
            message=f"{donation_obj.user.responsible}"
            + ", sua reserva de "
            + f"{donation_obj.quantity} "
            + "de "
            + f"{donation_obj.food} "
            + "foi reservada pela empresa "
            + f"{self.request.user.name}"
            + " e o "
            + f"{self.request.user.responsible}"
            + " irá entrar com contato com você.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[
                donation_obj.user.email,
            ],
            fail_silently=False,
        )


class ReservationDetailView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsCharity]

    queryset = Reservations.objects.all()
    serializer_class = ReservationDetailSerializer
    lookup_url_kwarg = "pk"

    @extend_schema(
        operation_id="delete_reservation_by_id",
        description="Rota para excluir a reserva pelo ID",
        summary="Exclui a reserva",
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ReservationCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsCharity]

    queryset = Reservations.objects.all()
    serializer_class = ReservationDetailCreateSerializer

    lookup_field = "pk"

    @extend_schema(
        operation_id="create_reservation_by_url_id",
        parameters=[
            ReservationDetailCreateSerializer,
        ],
        description="Rota para criação de reservas enviando id pela url",
        summary="Criação de reservas",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        donation_id = self.kwargs["pk"]
        donation_obj = get_object_or_404(Donations, id=donation_id)
        donation_obj.available = False

        obj = Donations.objects.get(pk=donation_id)
        obj.available = False
        obj.save()
        serializer.save(user=self.request.user, donation=donation_obj)

        send_mail(
            subject="Aviso de reserva de doação",
            message="Obrigado "
            + f"{self.request.user.responsible} "
            + "pela sua reserva de "
            + f"{donation_obj.quantity} "
            + "de "
            + f"{donation_obj.food}"
            + "! O responsável por essa doação é a empresa "
            + f"{donation_obj.user.name}"
            + " e você poderá entrar em contato com o "
            + f"{donation_obj.user.responsible} "
            + "no número "
            + f"{donation_obj.user.contact} "
            + "para proceder com a sua retirada da mercadoria reservada. O endereço é: "
            + f"{donation_obj.user.address.address}"
            + ", "
            + f"{donation_obj.user.address.complement}"
            + " na cidade de "
            + f"{donation_obj.user.address.city}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[
                self.request.user.email,
            ],
            fail_silently=False,
        )

        send_mail(
            subject="Aviso de reserva de doação",
            message=f"{donation_obj.user.responsible}"
            + ", sua reserva de "
            + f"{donation_obj.quantity} "
            + "de "
            + f"{donation_obj.food} "
            + "foi reservada pela empresa "
            + f"{self.request.user.name}"
            + " e o "
            + f"{self.request.user.responsible}"
            + " irá entrar com contato com você.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[
                donation_obj.user.email,
            ],
            fail_silently=False,
        )


class ReservationUserView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ReservationSerializer
    queryset = Reservations.objects.all()

    @extend_schema(
        operation_id="list_reservations_by_logged_charity",
        parameters=[
            ReservationSerializer,
        ],
        responses={201: ReservationSerializer},
        description="Rota para listagem de reservas do donatário logado",
        summary="Listagem de reservas",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
