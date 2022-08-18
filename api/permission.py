from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Model-level permission
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.user.is_authenticated or (request.method in permissions.SAFE_METHODS):
            # SAFE_METHODS(e.g.GET) is granted for both authenticated and non-authenticated users.
            # Other Methods are granted only for authenticated users.
            return True
        return False

    def has_object_permission(self, request, view, obj):
        """
           Object-level permission.
           Return `True` if permission is granted, `False` otherwise.
        """
        # SAFE_METHODS(e.g.GET) is granted for all users.
        # Other Methods are granted only for owner.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user


class IsUserOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to the user  to edit only his profile.
    """
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS(e.g.GET) is granted for all users.
        # Other Methods are granted only for user itself.
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user
