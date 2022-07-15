from rest_framework.permissions import IsAuthenticated

from users.models import UserRoles


class IsOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user and obj.author == request.user


class IsAdmin(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user.role == UserRoles.ADMIN
