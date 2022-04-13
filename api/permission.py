from rest_framework import permissions


class UserPostPermissions(permissions.BasePermission):
    # Owners of the object or admins can do anything with the object.
    # Others can do nothing except retrieve.

    def has_object_permission(self, request, view, obj):  # override the method
        return obj.author == request.user

