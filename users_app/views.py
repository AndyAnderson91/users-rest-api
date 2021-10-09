from rest_framework import generics
from django.contrib.auth.models import User
from users_app.serializers import UserSerializer
from rest_framework.permissions import AllowAny
from .permissions import IsAdminUserOrOwnerOrReadOnly


class UserListCreate(generics.ListCreateAPIView):
    """
    List all users or create a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Explicit is better than implicit.
    permission_classes = [AllowAny, ]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete User instance.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUserOrOwnerOrReadOnly, ]

    def perform_destroy(self, instance):
        """
        Set is_active attribute to False instead of deleting object.
        """
        instance.is_active = False
        instance.save()
