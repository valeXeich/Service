from rest_framework import permissions


class IsSpecialistOwnerOrAdmin(permissions.BasePermission):
    """Access for specialist and admin"""

    def has_permission(self, request, view):
        specialist = request.user.specialist_set.first()
        if request.user.is_staff:
            return True
        return specialist.user.slug == view.kwargs["slug"]


class IsClient(permissions.BasePermission):
    """Access for client"""

    def has_permission(self, request, view):
        return request.user.status == "client"

