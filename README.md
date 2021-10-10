# Users REST API
Simple API built with Django Rest Framework. Token-based Authentication is used.
## Main purpose:
Provide CRUD operations on user objects in database.
## Endpoints:
* **POST */api-token-auth/***
  * Create user authentication token;
  * Data: `{ 'username': str, 'password': str }` - both fields are required;
  * Response: `{ 'token': str }`, status code 200.
* **GET */api/users/***
  * List all users in database. Allowed to any user;
  * Response: `[ { 'id': int, 'username': str, 'first_name': str, 'last_name': str, 'is_active': bool, 'last_login': str, 'is_superuser': bool }, ]`, status code 200.
* **POST */api/users/***
  * Create a new user. Allowed to any user;
  * Data: `{ 'username': str, 'first_name': str, 'last_name': str, 'password': str, 'is_active': bool }` - username, password and is_active fields are required;
  * Response: `{ 'id': int, 'username': str, 'first_name': str, 'last_name': str, 'is_active': bool, 'last_login': str, 'is_superuser': bool }`, status code 201.
* **GET */api/users/{id}/***
  * Retrieve user object. Allowed to any user;
  * Id: unique integer value identifying user;
  * Response: `{ 'id': int, 'username': str, 'first_name': str, 'last_name': str, 'is_active': bool, 'last_login': str, 'is_superuser': bool }`, status code 200.
* **PUT */api/users/{id}/***
  * Update user object. Requires authentication. Allowed to account owner or admin user;
  * Id: unique integer value identifying user;
  * Data: `{ 'username': str, 'first_name': str, 'last_name': str, 'password': str, 'is_active': bool }` - username, password and is_active fields are required;
  * Response: `{ 'id': int, 'username': str, 'first_name': str, 'last_name': str, 'is_active': bool, 'last_login': str, 'is_superuser': bool }`, status code 200.
* **PATCH */api/users/{id}/***
  * Partially update user object. Requires authentication. Allowed to account owner or admin user;
  * Id: unique integer value identifying user;
  * Data: `{ 'username': str, 'first_name': str, 'last_name': str, 'password': str, 'is_active': bool }`;
  * Response: `{ 'id': int, 'username': str, 'first_name': str, 'last_name': str, 'is_active': bool, 'last_login': str, 'is_superuser': bool }`, status code 200.
* **DELETE */api/users/{id}/***
  * Set user object is_active field to False. Requires authentication. Allowed to account owner or admin user;
  * Id: unique integer value identifying user;
  * Response: status code 204.
## To run application on local machine:
#### 1. Clone the repository:
`git clone https://github.com/AndyAnderson91/users-rest-api.git && cd users-rest-api`
#### 2. Create a virtual environment:
`python3 -m venv venv`
#### 3. Activate the virtual environment:
`source venv/bin/activate`
#### 4. Install all required dependencies:
`pip install -r requirements.txt`
#### 5. Apply the migrations:
`python manage.py migrate`
#### 6. Create superuser:
`python manage.py createsuperuser`
#### 7. Run server:
`python manage.py runserver`
#### 8. From now local version is available at http://127.0.0.1:8000
## Testing:
Tests cover *serializers.py*, *permissions.py* and *views.py* modules. All tests are written with *pytest-django* plugin.
To run tests locally use:<br>
`pytest` command in terminal
## Credentials for [heroku version](https://users-rest-api-drf.herokuapp.com):
#### Admin:
* username: admin
* password: mypass123