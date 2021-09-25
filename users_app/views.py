from rest_framework import generics
from django.contrib.auth.models import User
from users_app.serializers import UserSerializer
from .permissions import CustomIsAuthenticated, CustomIsAdminUser, IsReadOnly, IsWriteOnly, IsActive, IsOwner


class ListCreateUserView(generics.ListCreateAPIView):
    """
    List all users or create a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [CustomIsAuthenticated & IsActive | IsWriteOnly]


class RetrieveUpdateDestroyUserView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete User instance.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        CustomIsAuthenticated &
        IsActive &
        (CustomIsAdminUser | IsOwner | IsReadOnly)
    ]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
