import pytest
from authentication.serializers import LoginSerializer

@pytest.mark.django_db
class TestLoginSerializer:

    def test_valid_data(self):
        data = {
            'email': 'test@example.com',
            'password': 'ValidPass123!'
        }
        serializer = LoginSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data['email'] == data['email']
        assert serializer.validated_data['password'] == data['password']

    def test_invalid_email_format(self):
        data = {
            'email': 'invalid-email',
            'password': 'ValidPass123!'
        }
        serializer = LoginSerializer(data=data)
        assert not serializer.is_valid()
        assert 'email' in serializer.errors

    def test_missing_email(self):
        data = {
            'password': 'ValidPass123!'
        }
        serializer = LoginSerializer(data=data)
        assert not serializer.is_valid()
        assert 'email' in serializer.errors

    def test_missing_password(self):
        data = {
            'email': 'test@example.com'
        }
        serializer = LoginSerializer(data=data)
        assert not serializer.is_valid()
        assert 'password' in serializer.errors
