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


class UserView(generics.ListCreateAPIView):

    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            self.authentication_classes = [JWTAuthentication]
            self.permission_classes = [IsAuthenticated, IsAdm]
        return super().dispatch(request, *args, **kwargs)

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrAdm]

    lookup_field = "pk"

    # def get(self, request, pk):
    #     user = get_object_or_404(User, pk=pk)
    #     self.check_object_permissions(request, user)
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)

    
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
        user.isActive = False
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

