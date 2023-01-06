from rest_framework import permissions
from users.models import User
from rest_framework.views import View


class IsCharity(permissions.BasePermission):
    def has_permission(self, request, view: View):
        return request.user.type == "charity" 


class IsOwnerOrAdm(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        return obj == request.user or request.user.isAdm