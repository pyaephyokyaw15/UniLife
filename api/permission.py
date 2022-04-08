from rest_framework import permissions


class UserPermissionsObj(permissions.BasePermission):
    """
        Owners of the object or admins can do anything.
        Everyone else can do nothing.
    """
    def has_object_permission(self, request, view, obj):

        return obj.owner == request.user

