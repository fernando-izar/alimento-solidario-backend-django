from rest_framework import permissions
from users.models import User
from rest_framework.views import View
from datetime import datetime
import ipdb
from rest_framework.exceptions import PermissionDenied


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: User) -> bool:
        return request.user.is_authenticated and obj == request.user

class IsDonor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.type == "donor"
        return True