from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth.models import User
from users_app.serializers import ReadOnlyUserSerializer, WriteOnlyUserSerializer


# class UsersList(generics.ListCreateAPIView):
#     """
#     List all users or create a new user.
#     """
#     queryset = User.objects.all()
#
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return WriteOnlyUserSerializer
#         return ReadOnlyUserSerializer


# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     """
#     Retrieve, update or delete User instance.
#     """
#     queryset = User.objects.all()
#
#     def get_serializer_class(self):
#         if self.request.method in ('PUT', 'PATCH'):
#             return WriteOnlyUserSerializer
#         return ReadOnlyUserSerializer
#
#     def delete(self, request, *args, **kwargs):
#         user = get_object_or_404(User, pk=kwargs.get('pk'))
#         user.is_active = False
#         user.save()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class UsersList(APIView):
    """
    List all users or create a new user.
    """
    def get(self, request, formant=None):
        users = User.objects.all()
        read_serializer = ReadOnlyUserSerializer(users, many=True)
        return Response(read_serializer.data)

    def post(self, request, format=None):
        write_serializer = WriteOnlyUserSerializer(data=request.data)
        if write_serializer.is_valid():
            user = write_serializer.save()
            read_serializer = ReadOnlyUserSerializer(user)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        return Response(write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    Retrieve, update or delete User instance.
    """
    def get(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        read_serializer = ReadOnlyUserSerializer(user)
        return Response(read_serializer.data)

    def put(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        write_serializer = WriteOnlyUserSerializer(user, data=request.data)
        if write_serializer.is_valid():
            write_serializer.save()
            read_serializer = ReadOnlyUserSerializer(user)
            return Response(read_serializer.data)
        return Response(write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        write_serializer = WriteOnlyUserSerializer(user, data=request.data, partial=True)
        if write_serializer.is_valid():
            write_serializer.save()
            read_serializer = ReadOnlyUserSerializer(user)
            return Response(read_serializer.data)
        return Response(write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
