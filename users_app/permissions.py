from rest_framework.permissions import BasePermission, SAFE_METHODS


class CustomIsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class CustomIsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsActive(BasePermission):
    """
    Allow access only to active users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsReadOnly(BasePermission):
    """
    Allows access to safe methods to any user.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsWriteOnly(BasePermission):
    """
    Allow access to post data to any user.
    """
    def has_permission(self, request, view):
        return request.method == 'POST'


class IsOwner(BasePermission):
    """
    Allow access to object's owner.
    """
    def has_object_permission(self, request, view, obj):
        print('YES IM HERE!!!!FML 17')
        return request.user == obj
