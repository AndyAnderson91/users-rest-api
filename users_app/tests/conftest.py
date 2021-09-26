import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


# Constants

ACTIVE_USER1_DATA = {'username': 'andy', 'password': 'mypass123', 'is_active': True}
ACTIVE_USER2_DATA = {'username': 'marie', 'password': 'mypass123', 'is_active': True}
INACTIVE_USER_DATA = {'username': 'jamie', 'password': 'mypass123', 'is_active': False}
ADMIN_USER_DATA = {'username': 'admin', 'password': 'mypass123', 'is_active': True}


# Fixtures

@pytest.fixture
def active_user1():
    return User.objects.create_user(**ACTIVE_USER1_DATA)


@pytest.fixture
def active_user2():
    return User.objects.create_user(**ACTIVE_USER2_DATA)


@pytest.fixture
def inactive_user():
    return User.objects.create_user(**INACTIVE_USER_DATA)


@pytest.fixture
def admin():
    return User.objects.create_superuser(**ADMIN_USER_DATA)


@pytest.fixture
def active_user1_token(active_user1):
    token, _ = Token.objects.get_or_create(user=active_user1)
    return token


@pytest.fixture
def active_user2_token(active_user2):
    token, _ = Token.objects.get_or_create(user=active_user2)
    return token


@pytest.fixture
def inactive_user_token(inactive_user):
    token, _ = Token.objects.get_or_create(user=inactive_user)
    return token


@pytest.fixture
def admin_token(admin):
    token, _ = Token.objects.get_or_create(user=admin)
    return token


@pytest.fixture
def active_user1_detail_url(active_user1):
    return reverse('user_detail', kwargs={'pk': active_user1.pk})


@pytest.fixture
def inactive_user_detail_url(inactive_user):
    return reverse('user_detail', kwargs={'pk': inactive_user.pk})


@pytest.fixture
def user_list_create_url():
    return reverse('user_list_create')


@pytest.fixture
def api_client():
    return APIClient()
