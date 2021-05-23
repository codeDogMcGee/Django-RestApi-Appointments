from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only allow owner to update or delete, anyone can read
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions
        # Always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions
        return obj.owner == request.user


class IsOwner(permissions.BasePermission):
    """
    Only allow owner to update or delete, or read
    """
    def has_object_permission(self, request, view, obj):
        # Write permissions
        return obj.owner == request.user
