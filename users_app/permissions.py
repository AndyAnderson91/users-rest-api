# !Important
# This approach with defining custom IsAuthenticated and IsAdmin classes
# with purpose of adding has_object_permission() method to them
# as well as adding has_object_permission() method to any other permission class
# is used to fix bitwise operations bug described here:
# https://github.com/encode/django-rest-framework/issues/7117
# https://github.com/encode/django-rest-framework/pull/7155
# The essence of bug is that implemented has_object_permission() method is not called
# if two or more classes combined by bitwise operators and:
# - one class implements has_permission() method only;
# - another one implements has_object_permission() method.

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
    Allow access to POST method to any user.
    """
    def has_permission(self, request, view):
        return request.method == 'POST'

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsOwner(BasePermission):
    """
    Allow access to object's owner.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj
