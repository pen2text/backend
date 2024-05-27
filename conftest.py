import uuid
from package_manager.models import PackagePlanDetails, PlanType
import pytest
from unittest.mock import patch
from datetime import date
from rest_framework.test import APIClient
from user_management.models import Users
from rest_framework_simplejwt.tokens import AccessToken
from utils.jwt_token_utils import generate_jwt_token


@pytest.fixture
def api_client():
    return APIClient()

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

@pytest.fixture
def mock_user_serializer_save(db):
    def _create_user(*args, **kwargs):
        user = Users(
            first_name=kwargs.get('first_name', 'Test'),
            last_name=kwargs.get('last_name', 'User'),
            gender=kwargs.get('gender', 'female'),
            date_of_birth=kwargs.get('date_of_birth', date(1995, 5, 20)),
            email=kwargs.get('email', 'test.user@example.com'),
            is_verified=kwargs.get('is_verified', False),
            role=kwargs.get('role', 'user')
        )
        user.set_password(kwargs.get('password', 'TestUser123!'))
        user.save()
        return user
    
    with patch('user_management.serializers.UserSerializer.save', side_effect=_create_user) as mock:
        yield mock

@pytest.fixture
def mock_jwt_token():
    def token(user, token_type):
        payload = {
            'email': user.email,
            'id': str(user.id),
            'token_type': token_type
        }
        return generate_jwt_token(payload)
    return token
 
@pytest.fixture
def package_plans(db):
    plan1 = PackagePlanDetails.objects.create(
        name='free',
        plan_type=PlanType.LIMITED_USAGE,
        usage_limit=10,
        price=0.00,
        days=1
    )
    plan2 = PackagePlanDetails.objects.create(
        name='free_unregistered',
        plan_type=PlanType.LIMITED_USAGE,
        usage_limit=10,
        price=0.00,
        days=7
    )
    return [plan1, plan2]
 
       
# @pytest.fixture
# def mock_user_serializer_save():
#     with patch('user_management.serializers.UserSerializer.save') as mock:
#         yield mock