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
        operation_id="create_user",
        parameters=[
            UserSerializer,
        ],
        request=UserSerializer,
        responses={201: UserSerializer},
        description="Rota para criação de usuários",
        summary="Criação de usuários",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @extend_schema(
        operation_id="list_users",
        parameters=[
            UserSerializer,
        ],
        responses={201: UserSerializer},
        description="Rota para listagem de usuários",
        summary="Listagem de usuários",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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
        operation_id="get_user_by_id",
        parameters=[
            UserSerializer,
        ],
        request=UserSerializer,
        responses={201: UserSerializer},
        description="Rota para mostrar o usuário pelo ID",
        summary="Mostra o usuário",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        operation_id="update_user_by_id",
        parameters=[
            UserSerializer,
        ],
        request=UserSerializer,
        responses={201: UserSerializer},
        description="Rota para atualizar o usuário pelo ID",
        summary="Atualiza o usuário",
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        exclude=True,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        operation_id="delete_user_by_id",
        description="Rota para excluir o usuário pelo ID",
        summary="Exclui o usuário",
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

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
        operation_id="list_user_profile",
        parameters=[
            UserSerializer,
        ],
        responses={201: UserSerializer},
        description="Rota para mostrar os dados do usuário logado",
        summary="Mostrar usuário logado",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class UserSoftDeleteView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrAdm]
    lookup_field = "pk"

    serializer_class = UserSerializer
    queryset = User.objects.all()

    @extend_schema(
        operation_id="soft_delete_user",
        parameters=[
            UserSerializer,
        ],
        request=UserSerializer,
        responses={201: UserSerializer},
        description="Rota para inativar o usuário",
        summary="Inativação do usuário",
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        exclude=True,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

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
