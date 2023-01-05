from rest_framework import permissions
from users.models import User
from rest_framework.views import View
from datetime import datetime
import ipdb


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: User) -> bool:
        return request.user.is_authenticated and obj == request.user

class IsDonor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.type == "donor"

class ValidatedExpiration(permissions.BasePermission):
    def has_permission(self, request, view):
        nowDate = datetime.now()
        dateFormat = f'{nowDate.year}-{nowDate.month}-{nowDate.day}'
        ipdb.set_trace()
        return request.data.expiration >= dateFormat