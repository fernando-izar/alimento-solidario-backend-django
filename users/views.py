from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdm, IsOwnerOrAdm
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .models import User
import ipdb
from django.views.generic import View
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt



class UserView(generics.ListCreateAPIView):

    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            self.authentication_classes = [JWTAuthentication]
            self.permission_classes = [IsAuthenticated, IsAdm]
        return super().dispatch(request, *args, **kwargs)

    queryset = User.objects.all()
    serializer_class = UserSerializer

class SoftDeleteUserView(View):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdm]

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user.isActive = False
        user.save()


    # queryset = User.objects.all()
    # serializer_class = UserSerializer

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    # def perform_destroy(self, instance):
    #     user = self.request.user

    #     if user == instance:
    #         instance.isActive = False
    #         instance.save()
    #     else:
    #         raise PermissionError("You can't delete other users")
        

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrAdm]

    
    


class UserProfileView(generics.ListAPIView):
    ...

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

