import pytest
import re
from datetime import date
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from user_management.models import Users
from user_management.serializers import UserUpdateSerializer

@pytest.fixture
def mock_request():
    factory = APIRequestFactory()
    request = factory.post('/fake-url/')
    return Request(request)

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

@pytest.mark.django_db
class TestUserUpdateSerializer:
    def test_validate_gender(self, mock_request, users):
        data = {'gender': 'invalid_gender'}
        user = users[0]
        serializer = UserUpdateSerializer(instance=user, data=data, context={'request': mock_request})
        assert not serializer.is_valid()
        assert 'gender' in serializer.errors
        assert serializer.errors['gender'][0].code == 'max_length' 

    def test_validate_password_weak(self, mock_request, users):
        data = {'password': 'weak'}
        user = users[0]
        serializer = UserUpdateSerializer(instance=user, data=data, context={'request': mock_request})
        assert not serializer.is_valid()
        assert 'password' in serializer.errors

    def test_validate_password_strong(self, mock_request, users):
        data = {'password': 'StrongPassword123!' , 'old_password': 'JaneDoe123!'}
        user = users[0]
        serializer = UserUpdateSerializer(instance=user, data=data, context={'request': mock_request})
        assert serializer.is_valid()

    def test_validate_password_and_old_password(self, mock_request, users):
        user = users[0]
        data = {'old_password': 'InvalidOldPassword123!', 'password': 'NewStrongPassword123!'}
        serializer = UserUpdateSerializer(instance=user, data=data, context={'request': mock_request})
        assert not serializer.is_valid()
        assert 'old_password' in serializer.errors

    def test_validate_password_and_old_password_valid(self, mock_request, users):
        user = users[0]
        data = {'old_password': 'JaneDoe123!', 'password': 'NewStrongPassword123!'}
        serializer = UserUpdateSerializer(instance=user, data=data, context={'request': mock_request})
        assert serializer.is_valid()

    def test_update_method(self, mock_request, users):
        user = users[0]
        data = {'first_name': 'JaneUpdated', 'last_name': 'DoeUpdated', 'gender': 'male', 'date_of_birth': date(1990, 5, 15)}
        serializer = UserUpdateSerializer(instance=user, data=data, context={'request': mock_request})
        assert serializer.is_valid()
        updated_user = serializer.save()
        assert updated_user.gender == 'male'
        assert updated_user.first_name == 'JaneUpdated'
        assert updated_user.last_name == 'DoeUpdated'

