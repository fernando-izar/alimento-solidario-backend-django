from rest_framework import permissions
from .models import User
from rest_framework.views import View

class IsAdm(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.isAdm

class IsOwnerOrAdm(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        return obj == request.user or request.user.isAdm