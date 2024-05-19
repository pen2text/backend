import pytest
from unittest.mock import patch
from datetime import date
from rest_framework.test import APIClient
from user_management.models import Users
from rest_framework_simplejwt.tokens import AccessToken



@pytest.fixture
def mock_users():
    return [
        Users(
            first_name='Jane',
            last_name='Doe',
            gender='Female',
            date_of_birth=date(1992, 5, 15),  # Use date instead of datetime
            email='jane.doe@example.com',
            password='JaneDoe123!',
            is_verified=True,
            role='admin'
        ),
        Users(
            first_name='John',
            last_name='Smith',
            gender='Male',
            date_of_birth=date(1990, 8, 20),  # Use date instead of datetime
            email='john.smith@example.com',
            password='JohnSmith123!',
            is_verified=True,
            role='user'
        ),
    ]

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def mock_send_verification_email():
    with patch('user_management.views.send_verification_email') as mock:
        yield mock

@pytest.fixture
def mock_user_serializer_save():
    with patch('user_management.serializers.UserSerializer.save') as mock:
        yield mock

@pytest.fixture
def users(db):
    user1 = Users.objects.create(
        first_name='Jane',
        last_name='Doe',
        gender='Female',
        date_of_birth=date(1992, 5, 15),
        email='jane.doe@example.com',
        is_verified=True,
        role='admin'
    )
    user1.set_password('JaneDoe123!')
    user1.save()

    user2 = Users.objects.create(
        first_name='John',
        last_name='Smith',
        gender='Male',
        date_of_birth=date(1990, 8, 20),
        email='john.smith@example.com',
        is_verified=True,
        role='user'
    )
    user2.set_password('JohnSmith123!')
    user2.save()

    user3 = Users.objects.create(
        first_name='Alice',
        last_name='Johnson',
        gender='Female',
        date_of_birth=date(1985, 1, 30),
        email='alice.johnson@example.com',
        is_verified=False,
        role='admin'
    )
    user3.set_password('AliceJohnson123!')
    user3.save()

    return [user1, user2, user3]

@pytest.fixture
def mock_token(mocker, users):
    def generate_token(user):
        token = AccessToken.for_user(user)
        mocker.patch('rest_framework_simplejwt.tokens.AccessToken.for_user', return_value=token)
        mocker.patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate', return_value=(user, token))
        return token
    return generate_token


# @pytest.fixture
# def mock_admin_user(mocker):
#     user = Users(
#         id='123e4567-e89b-12d3-a456-426614174000',
#         first_name='Admin',
#         last_name='User',
#         gender='Male',
#         date_of_birth=date(1990, 1, 1),
#         email='admin.user@example.com',
#         password='AdminUser123!',
#         is_verified=True,
#         role='admin'
#     )
#     mocker.patch('user_management.models.Users.objects.get', return_value=user)
#     return user

# @pytest.fixture
# def mock_user_user(mocker):
#     user = Users(
#         id='124e4567-e89b-12d3-a456-426614174001',
#         first_name='Regular',
#         last_name='User',
#         gender='Female',
#         date_of_birth=date(1992, 5, 15),
#         email='regular.user@example.com',
#         password='RegularUser123!',
#         is_verified=True,
#         role='user'
#     )
#     mocker.patch('user_management.models.Users.objects.get', return_value=user)
#     return user

# @pytest.fixture
# def mock_admin_token(mocker, mock_admin_user):
#     token = AccessToken.for_user(mock_admin_user)
#     mocker.patch('rest_framework_simplejwt.tokens.AccessToken.for_user', return_value=token)
#     mocker.patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate', return_value=(mock_admin_user, token))
#     return str(token)

# @pytest.fixture
# def mock_user_token(mocker, mock_user_user):
#     token = AccessToken.for_user(mock_user_user)
#     mocker.patch('rest_framework_simplejwt.tokens.AccessToken.for_user', return_value=token)
#     mocker.patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate', return_value=(mock_user_user, token))
#     return str(token)
