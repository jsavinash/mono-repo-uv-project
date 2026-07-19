from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    """Allow read-only access to everyone, but write access only to admins."""

    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(BasePermission):
    """Allow access only to the object owner or admin."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return hasattr(obj, "user") and obj.user == request.user
