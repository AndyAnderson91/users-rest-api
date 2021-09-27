from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserListCreatePermission(BasePermission):
    """
    Allows access to POST method to any user.
    Other methods are only allowed to active and authenticated users.
    """

    def has_permission(self, request, view):
        return bool(
            request.method == 'POST' or
            request.user and
            request.user.is_authenticated and
            request.user.is_active
        )


class UserDetailPermission(BasePermission):
    """
    Safe methods: allowed to active and authenticated users.
    Other methods: allowed to active and authenticated object's owner or admin.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_active
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user.is_staff or
            request.user == obj
        )
