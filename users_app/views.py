from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from users_app.serializers import ReadOnlyUserSerializer, WriteOnlyUserSerializer


class ListCreateUserView(APIView):
    """
    List all users or create a new user.
    """
    def get(self, request, formant=None):
        users = User.objects.all()
        read_serializer = ReadOnlyUserSerializer(users, many=True)
        return Response(read_serializer.data)

    def post(self, request, format=None):
        return write_and_response(data=request.data)


class RetrieveUpdateDestroyUserView(APIView):
    """
    Retrieve, update or delete User instance.
    """
    def get(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        read_serializer = ReadOnlyUserSerializer(user)
        return Response(read_serializer.data)

    def put(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        return write_and_response(user, data=request.data)

    def patch(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        return write_and_response(user, data=request.data, partial=True)

    def delete(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


def write_and_response(*write_serializer_args, **write_serializer_kwargs):
    write_serializer = WriteOnlyUserSerializer(*write_serializer_args, **write_serializer_kwargs)
    write_serializer.is_valid(raise_exception=True)
    instance = write_serializer.save()
    read_serializer = ReadOnlyUserSerializer(instance)
    return Response(read_serializer.data)
