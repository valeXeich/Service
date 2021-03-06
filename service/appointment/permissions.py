from rest_framework import permissions


class IsSpecialistOwnerOrAdmin(permissions.BasePermission):
    """Access for specialist and admin"""

    def has_permission(self, request, view):
        if request.user.is_authenticated is True and not request.user.specialist_set.exists():
            specialist = request.user.specialist_set.first()
        else:
            return False
        if request.user.is_staff:
            return True
        return specialist.id == request.data['specialist']


class IsSpecialistOwner(permissions.BasePermission):
    """Access for specialist"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if request.user.is_authenticated is True and not request.user.specialist_set.exists():
            specialist = request.user.specialist_set.first()
            return obj.specialist == specialist
        return False


class IsClient(permissions.BasePermission):
    """Access for client"""

    def has_permission(self, request, view):
        return request.user.is_authenticated is True and request.user.status == "client"

