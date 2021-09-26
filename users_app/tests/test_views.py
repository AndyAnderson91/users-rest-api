"""
This module contains tests for:
- UserCreateList view GET POST methods. (in tests titles UserCreateList shortcutted to ucl);
- UserDetail view GET PUT PATCH DELETE methods. (in tests titles UserDetail shortcutted to ud).
Since most of these methods (except DELETE) are inherited from built-in generic classes,
this module only contains few tests which will be helpful in case of future custom implementation.
"""

import pytest
import json
from django.contrib.auth.models import User


# Constants

POST_PUT_DATA = {'username': 'new_username', 'password': 'newpass123', 'is_active': True}
PATCH_DATA = {'username': 'new_username'}


# UserListCreate view GET method tests.

@pytest.mark.django_db
def test_ulc_get_method_return_list_of_all_users(api_client, user_list_create_url, active_user1, active_user2, inactive_user, admin_token):
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + admin_token.key)
    bytes_data = api_client.get(user_list_create_url).content
    users_list = json.loads(bytes_data.decode('utf-8'))
    # active_user1, active_user2, inactive_user and admin.
    assert len(users_list) == 4


# UserListCreate view POST method tests.

@pytest.mark.django_db
def test_ulc_post_method_create_new_user(api_client, user_list_create_url, admin_token):
    users_count_before_post = User.objects.count()
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + admin_token.key)
    api_client.post(user_list_create_url, data=POST_PUT_DATA)
    users_count_after_post = User.objects.count()
    assert users_count_after_post - users_count_before_post == 1


# UserDetail view GET method tests.

@pytest.mark.django_db
def test_ud_get_method_return_required_user_data(api_client, active_user1, active_user1_detail_url, active_user1_token):
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + active_user1_token.key)
    bytes_data = api_client.get(active_user1_detail_url).content
    user_data = json.loads(bytes_data.decode('utf-8'))
    assert user_data['username'] == active_user1.username


# UserDetail view PUT method tests.

@pytest.mark.django_db
def test_ud_put_method_update_required_user_data(api_client, active_user1, active_user1_detail_url, active_user1_token):
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + active_user1_token.key)
    api_client.put(active_user1_detail_url, data=POST_PUT_DATA)
    updated_user = User.objects.get(pk=active_user1.pk)
    assert updated_user.username == POST_PUT_DATA['username']


# UserDetail view PATCH method tests.

@pytest.mark.django_db
def test_ud_put_method_update_required_user_data(api_client, active_user1, active_user1_detail_url, active_user1_token):
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + active_user1_token.key)
    api_client.patch(active_user1_detail_url, data=PATCH_DATA)
    updated_user = User.objects.get(pk=active_user1.pk)
    assert updated_user.username == PATCH_DATA['username']


# UserDetail view DELETE method tests.

@pytest.mark.django_db
def test_user_detail_delete_method_set_user_is_active_to_false_instead_of_destroying_object(api_client, active_user1_detail_url, admin_token):
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + admin_token.key)
    api_client.delete(active_user1_detail_url)
    user = User.objects.get(is_staff=False)
    assert not user.is_active
