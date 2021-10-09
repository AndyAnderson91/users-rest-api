# Users REST API
Simple API built with Django Rest Framework. Token-based Authentication is used.
## Main purpose:
Provide CRUD operations on user objects in database.
## Endpoints:
* **POST */api-token-auth/***
  * Creates user's authentication token;
  * Data: `{ 'username': str, 'password': str }` - both fields required;
  * Response: `{ 'token': str }`, status code 200.
* **GET */api/users/***
  * List all users in database. Allowed to any user;
  * Response: `[ { 'id': int, 'username': str, 'first_name': str, 'last_name': str, 'is_active': bool, 'last_login': str, 'is_superuser': bool }, ]`, status code 200.
* **POST */api/users/***
  * Create a new user. Allowed to any user;
  * Data: `{ 'username': str, 'first_name': str, 'last_name': str, 'password': str, 'is_active': bool }` - username, password and is_active fields are required;
  * Response: `{ 'id': int, 'username': str, 'first_name': str, 'last_name': str, 'is_active': bool, 'last_login': str, 'is_superuser': bool }`, status code 201.
* **GET */api/users/{id}/***
  * Retrieve particular user. Allowed to any user;
  * Id: unique integer value identifying user;
  * Response: `{ 'id': int, 'username': str, 'first_name': str, 'last_name': str, 'is_active': bool, 'last_login': str, 'is_superuser': bool }`, status code 200.
* **PUT */api/users/{id}/***
  * Update user model. All required fields must be provided. Allowed to active authenticated account owner or admin;
  * Id: unique integer value identifying user;
  * Data: `{ 'username': str, 'first_name': str, 'last_name': str, 'password': str, 'is_active': bool }` - username, password and is_active fields are required;
  * Response: `{ 'id': int, 'username': str, 'first_name': str, 'last_name': str, 'is_active': bool, 'last_login': str, 'is_superuser': bool }`, status code 200.
* **PATCH */api/users/{id}/***
  * Update any user model field. Allowed to active authenticated account owner or admin;
  * Id: unique integer value identifying user;
  * Data: `{ 'username': str, 'first_name': str, 'last_name': str, 'password': str, 'is_active': bool }`;
  * Response: `{ 'id': int, 'username': str, 'first_name': str, 'last_name': str, 'is_active': bool, 'last_login': str, 'is_superuser': bool }`, status code 200.
* **DELETE */api/users/{id}/***
  * Set user's is_active field to False. Allowed to active authenticated account owner or admin;
  * Id: unique integer value identifying user;
  * Response: status code 204.
  ## Testing:
  Tests cover *serializers.py*, *permissions.py* and *views.py* modules. All tests are written with *pytest-django* plugin.
