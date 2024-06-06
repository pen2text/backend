import pytest
import re
from datetime import date
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from user_management.serializers import UserSerializer

@pytest.fixture
def mock_request():
    factory = APIRequestFactory()
    request = factory.post('/fake-url/')
    return Request(request)

@pytest.mark.django_db
class TestUserSerializer:
    def test_gender_validation_invalid(self, mock_request):
        data = {'gender': 'invalid_gender'}
        serializer = UserSerializer(data=data, context={'request': mock_request})
        assert not serializer.is_valid()
        assert 'gender' in serializer.errors
        assert serializer.errors['gender'][0].code == 'max_length' 

    def test_gender_validation_valid(self, mock_request):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'gender': 'female',
            'date_of_birth': date(1990, 5, 15),
            'email': 'john.doe@example.com',
            'password': 'StrongPassword123!',
        }
        serializer = UserSerializer(data=data, context={'request': mock_request})
        assert serializer.is_valid()

    def test_password_validation_weak(self, mock_request):
        data = {'password': 'weak'}
        serializer = UserSerializer(data=data, context={'request': mock_request})
        assert not serializer.is_valid()
        assert 'password' in serializer.errors

    def test_password_validation_strong(self, mock_request):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'gender': 'male',
            'date_of_birth': date(1990, 5, 15),
            'email': 'john.doe@example.com',
            'password': 'StrongPassword123!',
        }
        serializer = UserSerializer(data=data, context={'request': mock_request})
        assert serializer.is_valid()

    def test_save_method(self, mock_request):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'gender': 'male',
            'date_of_birth': date(1990, 5, 15),
            'email': 'john.doe@example.com',
            'password': 'StrongPassword123!',
            'is_verified': True,
            'role': 'user',
            'profile_picture_url': 'http://example.com/profile.jpg',
            'created_at': None,
            'updated_at': None
        }
        serializer = UserSerializer(data=data, context={'request': mock_request})
        assert serializer.is_valid()
        user = serializer.save()
        assert user.id is not None
