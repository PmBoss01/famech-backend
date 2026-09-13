from rest_framework.permissions import BasePermission

from users.models import Role


class IsOwnerRole(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == Role.OWNER
        )


class IsMechanicRole(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == Role.MECHANIC
        )


class IsRequestOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner_id == request.user.id


class IsJobMechanic(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.mechanic_id == request.user.id
