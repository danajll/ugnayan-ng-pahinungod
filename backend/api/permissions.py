from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Read-only access (GET, HEAD, OPTIONS) for anyone.
    Write access (POST, PUT, PATCH, DELETE) only for staff users.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)