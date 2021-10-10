from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminUserOrOwnerOrReadOnly(BasePermission):
    """
    Safe methods: allowed to any user.
    Other methods: allowed to account owner or admin.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return bool(
            request.user and
            (request.user.is_staff or request.user == obj)
        )
