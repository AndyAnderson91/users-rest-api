"""
This module contains tests for listed below permission classes:
    CustomIsAuthenticated,
    CustomIsAdminUser,
    IsReadOnly,
    IsWriteOnly,
    IsActive,
    IsOwner.
It tests if they applied and execute correctly in:
    UserCreateList view GET POST methods. (in tests titles UserCreateList shortcutted to ucl)
    UserDetail view GET PUT PATCH DELETE methods. (in tests titles UserDetail shortcutted to ud)
"""

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
PUT_DATA = {'username': 'new_name', 'password': 'newpass123', 'is_active': True}
PATCH_DATA = {'username': 'new_name'}


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


# UserListCreate view GET method tests

@pytest.mark.django_db
def test_ulc_get_method_is_not_allowed_to_unauthenticated_user(api_client, user_list_create_url):
    """
    Tests CustomIsAuthenticated permission applied.
    """
    response = api_client.get(user_list_create_url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_ulc_get_method_is_not_allowed_to_inactive_user(api_client, user_list_create_url, inactive_user_token):
    """
    Tests IsActive permission applied.
    """
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + inactive_user_token.key)
    response = api_client.get(user_list_create_url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_ulc_get_method_is_allowed_to_active_authenticated_user(api_client, user_list_create_url, active_user1_token):
    """
    Tests both CustomIsAuthenticated and IsActive permissions received.
    """
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + active_user1_token.key)
    response = api_client.get(user_list_create_url)
    assert response.status_code == 200


# UserListCreate view POST method tests.

@pytest.mark.django_db
def test_ulc_post_method_is_allowed_to_any_user(api_client, user_list_create_url):
    """
    Tests IsWriteOnly permission applied.
    """
    response = api_client.post(user_list_create_url, data=ACTIVE_USER1_DATA)
    assert response.status_code == 201


# UserDetail view GET method tests.

@pytest.mark.django_db
def test_ud_get_method_is_not_allowed_to_unauthenticated_user(api_client, active_user1_detail_url):
    """
    Tests CustomIsAuthenticated permission applied.
    """
    response = api_client.get(active_user1_detail_url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_ud_get_method_is_not_allowed_to_inactive_user(api_client, active_user1_detail_url, inactive_user_token):
    """
    Tests IsActive permission applied.
    """
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + inactive_user_token.key)
    response = api_client.get(active_user1_detail_url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_ud_get_method_is_allowed_to_active_authenticated_user(api_client, active_user1_detail_url, active_user2_token):
    """
    Tests CustomIsAuthenticated, IsActive and IsReadOnly permissions received.
    """
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + active_user2_token.key)
    response = api_client.get(active_user1_detail_url)
    assert response.status_code == 200


# UserDetail view PUT method tests.

@pytest.mark.django_db
def test_ud_put_method_is_not_allowed_to_unauthenticated_user(api_client, active_user1_detail_url):
    """
    Tests CustomIsAuthenticated permission applied.
    """
    response = api_client.put(active_user1_detail_url, data=PUT_DATA)
    assert response.status_code == 401


@pytest.mark.django_db
def test_ud_put_method_is_not_allowed_to_inactive_user(api_client, inactive_user_detail_url, inactive_user_token):
    """
    Tests IsActive permission applied.
    """
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + inactive_user_token.key)
    response = api_client.put(inactive_user_detail_url, data=PUT_DATA)
    assert response.status_code == 401


@pytest.mark.django_db
def test_ud_put_method_is_not_allowed_to_not_owner(api_client, active_user1_detail_url, active_user2_token):
    """
    Tests IsOwner permission applied.
    """
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + active_user2_token.key)
    response = api_client.put(active_user1_detail_url, data=PUT_DATA)
    assert response.status_code == 403


@pytest.mark.django_db
def test_ud_put_method_is_allowed_to_active_authenticated_owner(api_client, active_user1_detail_url, active_user1_token):
    """
    Tests CustomIsAuthenticated, IsActive and IsOwner permissions received.
    """
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + active_user1_token.key)
    response = api_client.put(active_user1_detail_url, data=PUT_DATA)
    assert response.status_code == 200


@pytest.mark.django_db
def test_ud_put_method_is_allowed_to_admin(api_client, active_user1_detail_url, admin_token):
    """
    Tests CustomIsAdmin permission applied.
    """
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + admin_token.key)
    response = api_client.put(active_user1_detail_url, data=PUT_DATA)
    assert response.status_code == 200


# UserDetail view PATCH method tests.

@pytest.mark.django_db
def test_ud_patch_method_is_not_allowed_to_unauthenticated_user(api_client, active_user1_detail_url):
    """
    Tests CustomIsAuthenticated permission applied.
    """
    response = api_client.patch(active_user1_detail_url, data=PATCH_DATA)
    assert response.status_code == 401


@pytest.mark.django_db
def test_ud_patch_method_is_not_allowed_to_inactive_user(api_client, inactive_user_detail_url, inactive_user_token):
    """
    Tests IsActive permission applied.
    """
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + inactive_user_token.key)
    response = api_client.patch(inactive_user_detail_url, data=PATCH_DATA)
    assert response.status_code == 401


@pytest.mark.django_db
def test_ud_patch_method_is_not_allowed_to_not_owner(api_client, active_user1_detail_url, active_user2_token):
    """
    Tests IsOwner permission applied.
    """
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + active_user2_token.key)
    response = api_client.patch(active_user1_detail_url, data=PATCH_DATA)
    assert response.status_code == 403


@pytest.mark.django_db
def test_ud_patch_method_is_allowed_to_active_authenticated_owner(api_client, active_user1_detail_url, active_user1_token):
    """
    Tests CustomIsAuthenticated, IsActive and IsOwner permissions received.
    """
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + active_user1_token.key)
    response = api_client.patch(active_user1_detail_url, data=PATCH_DATA)
    assert response.status_code == 200


@pytest.mark.django_db
def test_ud_patch_method_is_allowed_to_admin(api_client, active_user1_detail_url, admin_token):
    """
    Tests CustomIsAdmin permission applied.
    """
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + admin_token.key)
    response = api_client.patch(active_user1_detail_url, data=PATCH_DATA)
    assert response.status_code == 200


# UserDetail view DELETE method tests.

@pytest.mark.django_db
def test_ud_delete_method_is_not_allowed_to_unauthenticated_user(api_client, active_user1_detail_url):
    """
    Tests CustomIsAuthenticated permission applied.
    """
    response = api_client.delete(active_user1_detail_url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_ud_delete_method_is_not_allowed_to_inactive_user(api_client, inactive_user_detail_url, inactive_user_token):
    """
    Tests IsActive permission applied.
    """
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + inactive_user_token.key)
    response = api_client.delete(inactive_user_detail_url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_ud_delete_method_is_not_allowed_to_not_owner(api_client, active_user1_detail_url, active_user2_token):
    """
    Tests IsOwner permission applied.
    """
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + active_user2_token.key)
    response = api_client.delete(active_user1_detail_url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_ud_delete_method_is_allowed_to_active_authenticated_owner(api_client, active_user1_detail_url, active_user1_token):
    """
    Tests CustomIsAuthenticated, IsActive and IsOwner permissions received.
    """
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + active_user1_token.key)
    response = api_client.delete(active_user1_detail_url)
    assert response.status_code == 204


@pytest.mark.django_db
def test_ud_delete_method_is_allowed_to_admin(api_client, active_user1_detail_url, admin_token):
    """
    Tests CustomIsAdmin permission applied.
    """
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + admin_token.key)
    response = api_client.delete(active_user1_detail_url)
    assert response.status_code == 204
