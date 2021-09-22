from rest_framework import serializers
from django.contrib.auth import password_validation
from django.contrib.auth.models import User


class ReadOnlyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'is_active', 'last_login', 'is_superuser']
        extra_kwargs = {
            'first_name': {'max_length': 30},
            'is_active': {'required': True},
        }


class WriteOnlyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'is_active']
        extra_kwargs = {
            'first_name': {'max_length': 30},
            'is_active': {'required': True},
        }

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value
