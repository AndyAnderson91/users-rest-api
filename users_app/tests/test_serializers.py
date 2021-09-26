import pytest
from datetime import datetime
from django.contrib.auth.models import User
from users_app.serializers import UserSerializer


COMPLETE_DATA = {'username': 'andy', 'password': 'mypass123', 'is_active': True}

INCOMPLETE_DATA = [
    {'username': 'andy', 'password': 'mypass123'},
    {'username': 'andy', 'is_active': True},
    {'password': 'mypass123', 'is_active': True},
]

BAD_PASSWORD_DATA = [
    {'username': 'andy', 'password': '', 'is_active': True},
    {'username': 'andy', 'password': 'a', 'is_active': True},
    {'username': 'andy', 'password': 'qwerty', 'is_active': True},
    {'username': 'andy', 'password': '583457082345', 'is_active': True},
]


@pytest.mark.django_db
def test_serializer_is_valid_if_required_fields_passed():
    serializer = UserSerializer(data=COMPLETE_DATA)
    assert serializer.is_valid()


@pytest.mark.django_db
@pytest.mark.parametrize('incomplete_data', INCOMPLETE_DATA)
def test_serializer_is_not_valid_if_any_required_field_is_missing(incomplete_data):
    serializer = UserSerializer(data=incomplete_data)
    assert not serializer.is_valid()


@pytest.mark.django_db
def test_serializer_contains_expected_read_fields():
    user = User.objects.create_user(**COMPLETE_DATA)
    serializer = UserSerializer(user)
    assert set(serializer.data) == {
        'id',
        'username',
        'first_name',
        'last_name',
        'is_active',
        'last_login',
        'is_superuser'
    }


@pytest.mark.django_db
def test_read_only_fields_cant_be_written():
    read_only_fields = {'id': 150, 'last_login': datetime.now(), 'is_superuser': False}
    data = {**COMPLETE_DATA, **read_only_fields}
    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    assert set(serializer.validated_data) == set(COMPLETE_DATA)


@pytest.mark.django_db
@pytest.mark.parametrize('bad_password_data', BAD_PASSWORD_DATA)
def test_password_validation_is_set(bad_password_data):
    serializer = UserSerializer(data=bad_password_data)
    assert not serializer.is_valid()


@pytest.mark.django_db
def test_password_is_hashed_on_user_creation():
    serializer = UserSerializer(data=COMPLETE_DATA)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    created_user = User.objects.first()
    assert created_user.password.startswith('pbkdf2_sha')


@pytest.mark.django_db
def test_password_is_hashed_on_user_update():
    user = User.objects.create_user(**COMPLETE_DATA)
    update_data = {'password': 'newpass123'}
    serializer = UserSerializer(user, data=update_data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    assert user.password.startswith('pbkdf2_sha')
