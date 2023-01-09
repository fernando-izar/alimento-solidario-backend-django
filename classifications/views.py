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

    @extend_schema(
        operation_id="create_classification",
        parameters=[
            ClassificationSerializer,
        ],
        request=ClassificationSerializer,
        responses={201: ClassificationSerializer},
        description="Rota para criação de classificação",
        summary="Criação de classificação",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @extend_schema(
        operation_id="list_classification",
        parameters=[
            ClassificationSerializer,
        ],
        responses={201: ClassificationSerializer},
        description="Rota para listagem de classificações",
        summary="Listagem de classificações",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ClassificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdm]

    queryset = Classification.objects.all()
    serializer_class = ClassificationSerializer

    @extend_schema(
        operation_id="get_classification_by_id",
        parameters=[
            ClassificationSerializer,
        ],
        request=ClassificationSerializer,
        responses={201: ClassificationSerializer},
        description="Rota para mostrar a classificação pelo ID",
        summary="Mostra a classificação",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        operation_id="update_classification_by_id",
        parameters=[
            ClassificationSerializer,
        ],
        request=ClassificationSerializer,
        responses={201: ClassificationSerializer},
        description="Rota para atualizar a classificação pelo ID",
        summary="Atualiza a classificação",
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        exclude=True,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        operation_id="delete_classification_by_id",
        description="Rota para excluir a classificação pelo ID",
        summary="Exclui a classificação",
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ClassificationNameView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Classification.objects.all()
    serializer_class = ClassificationSerializer
    lookup_field = "name"

    @extend_schema(
        operation_id="get_classification_by_name",
        parameters=[
            ClassificationSerializer,
        ],
        request=ClassificationSerializer,
        responses={201: ClassificationSerializer},
        description="Rota para mostrar a classificação pelo nome",
        summary="Mostra a classificação pelo nome",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
