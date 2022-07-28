from rest_framework import permissions


# class IsOwnerOrReadOnly(permissions.BasePermission):
#     """
#     Object-level permission to only allow owners of an object to edit it.
#     Assumes the model instance has an `owner` attribute.
#     """
#
#     def has_object_permission(self, request, view, obj):
#         # Read permissions are allowed to any request,
#         # so we'll always allow GET, HEAD or OPTIONS requests.
#         if request.method in permissions.SAFE_METHODS:
#             return True
#
#         # Instance must have an attribute named `owner`.
#         return obj.owner == request.user

class UserPostPermissions(permissions.BasePermission):
    # Owners of the object or admins can do anything with the object.
    # Others can do nothing except retrieve.

    def has_object_permission(self, request, view, obj):  # override the method
        return obj.author == request.user

class UserCommentPermissions(permissions.BasePermission):
    # Owners of the object or admins can do anything with the object.
    # Others can do nothing except retrieve.

    def has_object_permission(self, request, view, obj):  # override the method
        return obj.owner == request.user

