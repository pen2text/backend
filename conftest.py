import pytest
from unittest.mock import patch
from datetime import date
from rest_framework.test import APIClient
from user_management.models import Users
from rest_framework_simplejwt.tokens import AccessToken


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
        gender='female',
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
        gender='male',
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
        gender='female',
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

