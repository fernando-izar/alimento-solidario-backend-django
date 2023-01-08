from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdm, IsOwnerOrAdm
from rest_framework import generics, status, request, response
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        operation_id="list_create_user",
        parameters=[
            UserSerializer,
            OpenApiParameter("pk", OpenApiTypes.UUID, OpenApiParameter.PATH),
            OpenApiParameter("queryparam1", OpenApiTypes.UUID, OpenApiParameter.QUERY),
        ],
        request=UserSerializer,
        responses={201: UserSerializer},
        description="Rota para listagem e criação de animais",
        # summary="Criação de animais",
        deprecated=True,  # (7)
        tags=["Users"],  # (8)
        # exclude=True,
    )
    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            self.authentication_classes = [JWTAuthentication]
            self.permission_classes = [IsAuthenticated, IsAdm]
        return super().dispatch(request, *args, **kwargs)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrAdm]

    lookup_field = "pk"

    @extend_schema(
        operation_id="list_create_user",
        parameters=[
            UserSerializer,
            OpenApiParameter("pk", OpenApiTypes.UUID, OpenApiParameter.PATH),
            OpenApiParameter("queryparam1", OpenApiTypes.UUID, OpenApiParameter.QUERY),
        ],
        request=UserSerializer,
        responses={201: UserSerializer},
        description="Rota para listagem e criação de animais",
        # summary="Criação de animais",
        deprecated=True,  # (7)
        tags=["Users"],  # (8)
        # exclude=True,
    )
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if not user.isActive:
            return Response(
                {"error": "User already deleted"}, status=status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)


class UserProfileView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        operation_id="list_create_user",
        parameters=[
            UserSerializer,
            OpenApiParameter("pk", OpenApiTypes.UUID, OpenApiParameter.PATH),
            OpenApiParameter("queryparam1", OpenApiTypes.UUID, OpenApiParameter.QUERY),
        ],
        request=UserSerializer,
        responses={201: UserSerializer},
        description="Rota para listagem e criação de animais",
        # summary="Criação de animais",
        deprecated=True,  # (7)
        tags=["Users"],  # (8)
        # exclude=True,
    )
    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class UserSoftDeleteView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrAdm]
    lookup_field = "pk"

    serializer_class = UserSerializer
    queryset = User.objects.all()

    @extend_schema(
        operation_id="list_create_user",
        parameters=[
            UserSerializer,
            OpenApiParameter("pk", OpenApiTypes.UUID, OpenApiParameter.PATH),
            OpenApiParameter("queryparam1", OpenApiTypes.UUID, OpenApiParameter.QUERY),
        ],
        request=UserSerializer,
        responses={201: UserSerializer},
        description="Rota para listagem e criação de animais",
        # summary="Criação de animais",
        deprecated=True,  # (7)
        tags=["Users"],  # (8)
        # exclude=True,
    )
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if not user.isActive:
            return Response(
                {"error": "User already deleted"}, status=status.HTTP_400_BAD_REQUEST
            )
        user.isActive = False
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
