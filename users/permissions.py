from rest_framework import permissions
from .models import User
from rest_framework.views import View


class IsAdm(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.isAdm


class IsOwnerOrAdm(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        print((str(view.kwargs["pk"])) == (str(request.user.id)))
        return str(view.kwargs["pk"]) == str(request.user.id) or request.user.isAdm