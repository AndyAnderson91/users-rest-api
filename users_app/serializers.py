from rest_framework import serializers
from django.contrib.auth import password_validation
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'is_active',
            'last_login',
            'is_superuser',
        ]
        read_only_fields = [
            'id',
            'last_login',
            'is_superuser',
        ]
        extra_kwargs = {
            'is_active': {'required': True},
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        """
        Create new user object with helper function.
        """
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Update user object fields values. Use helper function to update password.
        """
        for key, value in validated_data.items():
            if key == 'password':
                instance.set_password(value)
            else:
                setattr(instance, key, value)
        instance.save()
        return instance

    def validate_password(self, value):
        """
        Validate password field.
        """
        password_validation.validate_password(value, self.instance)
        return value
