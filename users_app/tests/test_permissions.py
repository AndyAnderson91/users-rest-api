"""
This module contains tests for listed below permission classes:
- CustomIsAuthenticated,
- CustomIsAdminUser,
- IsReadOnly,
- IsWriteOnly,
- IsActive,
- IsOwner.
Tests if these permission classes applied and execute correctly in:
- UserCreateList view (in tests titles UserCreateList shortcutted to ucl);
- UserDetail view (in tests titles UserDetail shortcutted to ud).
Tests are grouped by HTTP methods.
"""

import pytest


# Constants

PUT_DATA = {'username': 'new_username', 'password': 'newpass123', 'is_active': True}
PATCH_DATA = {'username': 'new_username'}


# UserListCreate view GET method tests.

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
    response = api_client.post(user_list_create_url, data=PUT_DATA)
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
