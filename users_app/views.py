from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from users_app.serializers import ReadOnlyUserSerializer, WriteOnlyUserSerializer


@api_view(['GET', 'POST'])
def users_list(request, format=None):
    """
    List all users, or create a new user.
    """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = ReadOnlyUserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        write_serializer = WriteOnlyUserSerializer(data=request.data)
        if write_serializer.is_valid():
            write_serializer.save()
            user = User.objects.get(username=request.data['username'])
            read_serializer = ReadOnlyUserSerializer(user)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        return Response(write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def user_detail(request, pk, format=None):
    """
    Retrieve, update or delete a user.
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        read_serializer = ReadOnlyUserSerializer(user)
        return Response(read_serializer.data)

    elif request.method in ('PUT', 'PATCH'):
        partial = True if request.method == 'PATCH' else False
        write_serializer = WriteOnlyUserSerializer(user, data=request.data, partial=partial)
        if write_serializer.is_valid():
            write_serializer.save()
            read_serializer = ReadOnlyUserSerializer(user)
            return Response(read_serializer.data)
        return Response(write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
