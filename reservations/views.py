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
        serializer.save(user=self.request.user, donation=donation_obj)


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
        description="Rota para criação de reservas enviando id ela url",
        summary="Criação de reservas",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        donation_id = self.kwargs["pk"]
        donation_obj = get_object_or_404(Donations, id=donation_id)

        serializer.save(user=self.request.user, donation=donation_obj)


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
