from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdm
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .models import User


class UserView(generics.ListCreateAPIView):

    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            self.authentication_classes = [JWTAuthentication]
            self.permission_classes = [IsAuthenticated, IsAdm]
        return super().dispatch(request, *args, **kwargs)

    queryset = User.objects.all()
    serializer_class = UserSerializer


class SoftDeleteUserView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        user = self.request.user

        if user == instance:
            instance.isActive = False
            instance.save()
        else:
            raise PermissionError("You can't delete other users")
        
    
        

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    ...


class UserProfileView(generics.ListAPIView):
    ...


class UserSoftDeleteView(generics.UpdateAPIView):
    ...
