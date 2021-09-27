# Users REST API
Simple API built with Django Rest Framework. Token-based Authentication is used.
## Main purpose:
Provide CRUD operations on user objects in database.
## Endpoints:
* **POST */api-token-auth/***
  * Creates user's authentication token;
  * Data: `{ 'username': str, 'password': str }` - both fields required;
  * Response: `{ 'token': str }`, status code 200.
* **GET */api/v1/users/***
  * List all users in database. Allowed to active authenticated users;
  * Response: `[ { 'id': int, 'username': str, 'first_name': str, 'last_name': str, 'is_active': bool, 'last_login': str, 'is_superuser': bool }, ]`, status code 200.
* **POST */api/v1/users/***
  * Create a new user. This method is allowed to anyone;
  * Data: `{ 'username': str, 'first_name': str, 'last_name': str, 'password': str, 'is_active': bool }` - username, password and is_active fields are required;
  * Response: `{ 'id': int, 'username': str, 'first_name': str, 'last_name': str, 'is_active': bool, 'last_login': str, 'is_superuser': bool }`, status code 201.
* **GET */v1/users/{id}/***
  * Retrieve particular user. Allowed to active authenticated users;
  * Id: unique integer value identifying user;
  * Response: `{ 'id': int, 'username': str, 'first_name': str, 'last_name': str, 'is_active': bool, 'last_login': str, 'is_superuser': bool }`, status code 200.
* **PUT */api/v1/users/{id}/***
  * Update user model. All required fields must be provided. Allowed to active authenticated object owner or admin;
  * Id: unique integer value identifying user;
  * Data: `{ 'username': str, 'first_name': str, 'last_name': str, 'password': str, 'is_active': bool }` - username, password and is_active fields are required;
  * Response: `{ 'id': int, 'username': str, 'first_name': str, 'last_name': str, 'is_active': bool, 'last_login': str, 'is_superuser': bool }`, status code 200.
* **PATCH */api/v1/users/{id}/***
  * Update any user model field. Allowed to active authenticated object owner or admin;
  * Id: unique integer value identifying user;
  * Data: `{ 'username': str, 'first_name': str, 'last_name': str, 'password': str, 'is_active': bool }`;
  * Response: `{ 'id': int, 'username': str, 'first_name': str, 'last_name': str, 'is_active': bool, 'last_login': str, 'is_superuser': bool }`, status code 200.
* **DELETE */api/v1/users/{id}/***
  * Set user's is_active field to False. Allowed to active authenticated object owner or admin;
  * Id: unique integer value identifying user;
  * Response: status code 204.
  ## Testing:
  Tests cover *serializers.py*, *permissions.py* and *views.py* modules. All tests are written with *pytest-django* plugin.
